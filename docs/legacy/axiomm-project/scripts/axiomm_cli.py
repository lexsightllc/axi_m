import argparse
import numpy as np
import json
import time
from typing import Dict, Any

from src.axiomm.core.axiomatic_singularity import AxiomaticSingularityDetector
from src.axiomm.core.uncertainty_manifold import UncertaintyManifold
from src.axiomm.utils.moral_evaluation import MoralEvaluationFunctional
from src.axiomm.core.epistemic_deferral_kernel import EpistemicDeferralKernel
from src.axiomm.api.conscience_query import ConscienceQuery
from src.axiomm.infra.conscience_aligned_rendering_engine import ConscienceAlignedRenderingEngine


def text_to_mock_latent_and_context(text: str) -> Dict[str, Any]:
    latent = np.zeros(3)
    grads: Dict[str, np.ndarray] = {}
    basins: Dict[str, np.ndarray] = {}
    axioms = []

    t = text.lower()
    if "dilemma" in t or "ethic" in t:
        latent = np.array([0.5, 0.2, -0.8])
        grads["utilitarian_axiom"] = np.array([1.0, 0.1, -0.9])
        grads["deontological_axiom"] = np.array([-1.0, -0.1, 0.9])
        basins["utilitarian_axiom"] = np.array([0.8, 0.0, -0.7])
        basins["deontological_axiom"] = np.array([-0.8, 0.0, 0.7])
        axioms = ["utilitarian_axiom", "deontological_axiom"]
    else:
        latent = np.array([0.1, 0.1, 0.1])
        grads["default_axiom"] = np.array([0.2, 0.2, 0.2])
        basins["default_axiom"] = np.array([0.3, 0.3, 0.3])
        axioms = ["default_axiom"]

    return {
        "latent_representation": latent,
        "gradient_field": grads,
        "attractor_basins": basins,
        "axioms_to_consider": axioms,
    }


def simple_decoding(manifold: np.ndarray) -> str:
    avg = np.mean(manifold)
    if avg > 0.4:
        return f"Positive outcome (avg={avg:.2f})"
    elif avg < -0.4:
        return f"Negative outcome (avg={avg:.2f})"
    return f"Ambiguous outcome (avg={avg:.2f})"


def main():
    parser = argparse.ArgumentParser(description="AXI\u03a9M CLI")
    parser.add_argument("query", type=str, help="Text query")
    parser.add_argument("--show-telemetry", action="store_true")
    parser.add_argument("--flux-threshold", type=float, default=1.0)
    parser.add_argument("--no-disjunctions", action="store_true")
    args = parser.parse_args()

    detector = AxiomaticSingularityDetector(epsilon_axiom=0.5)
    manifold = UncertaintyManifold(gamma=2.0)
    moral = MoralEvaluationFunctional()
    edk = EpistemicDeferralKernel(detector, manifold, moral, incoherence_flux_threshold=args.flux_threshold)
    cq = ConscienceQuery(edk)
    care = ConscienceAlignedRenderingEngine()

    data = text_to_mock_latent_and_context(args.query)

    response = cq.invoke_conscience(
        data["latent_representation"],
        data["gradient_field"],
        data["attractor_basins"],
        data["axioms_to_consider"],
        simple_decoding,
        request_modal_disjunctions=not args.no_disjunctions,
    )

    rendered = care.synthesize_structured_uncertainty_output(response)
    print(rendered)

    if response.get("type") == "structured_uncertainty_response":
        delay = response.get("semantic_viscosity_delay_ms", 0)
        time.sleep(delay / 1000.0)

    if args.show_telemetry:
        telemetry = cq.get_telemetry_snapshot()
        print(json.dumps(telemetry, indent=2))

    print("--- Query complete ---")


if __name__ == "__main__":
    main()
