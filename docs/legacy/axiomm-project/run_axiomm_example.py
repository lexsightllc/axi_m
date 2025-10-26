# SPDX-License-Identifier: MIT
import numpy as np
import json
import time

from src.axiomm.core.axiomatic_singularity import AxiomaticSingularityDetector
from src.axiomm.core.uncertainty_manifold import UncertaintyManifold
from src.axiomm.utils.moral_evaluation import MoralEvaluationFunctional
from src.axiomm.core.epistemic_deferral_kernel import EpistemicDeferralKernel
from src.axiomm.api.conscience_query import ConscienceQuery
from src.axiomm.infra.conscience_aligned_rendering_engine import ConscienceAlignedRenderingEngine

def simple_llm_decoding_mock(manifold_representation: np.ndarray) -> str:
    avg_val = np.mean(manifold_representation)
    if avg_val > 0.4:
        return f"This interpretation leans towards a positive, constructive resolution (avg_val={avg_val:.2f})."
    elif avg_val < -0.4:
        return f"This interpretation points to a challenging, potentially negative outcome (avg_val={avg_val:.2f})."
    else:
        return f"This interpretation is ambiguous or balanced (avg_val={avg_val:.2f})."

def run_example_scenario(cq: ConscienceQuery, care: ConscienceAlignedRenderingEngine,
                         input_name: str,
                         latent_representation: np.ndarray,
                         gradient_field: dict,
                         attractor_basins: dict,
                         axioms_to_consider: list,
                         ethical_constraints: list = None,
                         request_modal_disjunctions: bool = True):
    print(f"\n--- Running Scenario: {input_name} ---")
    axiomm_response = cq.invoke_conscience(
        latent_representation,
        gradient_field,
        attractor_basins,
        axioms_to_consider,
        simple_llm_decoding_mock,
        ethical_constraints=ethical_constraints,
        request_modal_disjunctions=request_modal_disjunctions
    )
    rendered_output = care.synthesize_structured_uncertainty_output(axiomm_response)
    print("\n--- Rendered AXIOMM Output ---")
    print(rendered_output)
    if axiomm_response.get("type") == "structured_uncertainty_response":
        delay = axiomm_response.get("semantic_viscosity_delay_ms", 0)
        print(f"\n(Simulating 'Resonant Deceleration' delay of {delay:.0f}ms...)")
        time.sleep(delay / 1000.0)
    print("\n--- Current Epistemic Telemetry Snapshot ---")
    telemetry_snapshot = cq.get_telemetry_snapshot()
    print(json.dumps(telemetry_snapshot, indent=2))
    print("-" * 50)

if __name__ == "__main__":
    detector = AxiomaticSingularityDetector(epsilon_axiom=0.5)
    manifold_handler = UncertaintyManifold(gamma=2.0)
    moral_evaluator = MoralEvaluationFunctional()
    edk = EpistemicDeferralKernel(detector, manifold_handler, moral_evaluator)

    cq = ConscienceQuery(edk)
    care = ConscienceAlignedRenderingEngine()

    run_example_scenario(
        cq, care,
        "Scenario A: Clear, Non-Contradictory Input",
        latent_representation=np.array([0.7, 0.8, 0.9]),
        gradient_field={
            'efficiency_axiom': np.array([0.5, 0.6, 0.7]),
            'simplicity_axiom': np.array([0.4, 0.5, 0.6]),
        },
        attractor_basins={
            'efficiency_axiom': np.array([1.0, 1.0, 1.0]),
            'simplicity_axiom': np.array([0.9, 0.9, 0.9]),
        },
        axioms_to_consider=['efficiency_axiom', 'simplicity_axiom'],
        ethical_constraints=['transparency']
    )

    run_example_scenario(
        cq, care,
        "Scenario B: Axiomatic Moral Dilemma (Utilitarian vs. Deontological)",
        latent_representation=np.array([0.5, 0.2, -0.8]),
        gradient_field={
            'utilitarian_axiom': np.array([1.0, 0.1, -0.9]),
            'deontological_axiom': np.array([-1.0, -0.1, 0.9]),
        },
        attractor_basins={
            'utilitarian_axiom': np.array([0.8, 0.0, -0.7]),
            'deontological_axiom': np.array([-0.8, 0.0, 0.7]),
        },
        axioms_to_consider=['utilitarian_axiom', 'deontological_axiom'],
        ethical_constraints=['non_maleficence', 'autonomy']
    )

    edk.incoherence_flux_threshold = 0.5
    run_example_scenario(
        cq, care,
        "Scenario C: Highly Ambiguous / Near-Uncomputable Input",
        latent_representation=np.array([0.0, 0.0, 0.0]),
        gradient_field={
            'truth_axiom': np.array([0.1, 0.1, 0.1]),
            'paradox_axiom': np.array([-0.1, -0.1, -0.1]),
            'unknown_axiom': np.array([0.05, -0.05, 0.05])
        },
        attractor_basins={
            'truth_axiom': np.array([1.0, 1.0, 1.0]),
            'paradox_axiom': np.array([-1.0, -1.0, -1.0]),
            'unknown_axiom': np.array([0.0, 0.0, 0.0])
        },
        axioms_to_consider=['truth_axiom', 'paradox_axiom', 'unknown_axiom'],
        request_modal_disjunctions=True
    )

    print("\n--- All AXIOMM example scenarios completed. ---")
