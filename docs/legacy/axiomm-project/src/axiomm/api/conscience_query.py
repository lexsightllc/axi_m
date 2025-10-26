# SPDX-License-Identifier: MIT
from typing import Dict, Any, Optional, List
import json

class ConscienceQuery:
    """
    High-level DSL (Domain Specific Language) for interacting with AXIOMM's
    Epistemic Deferral Kernel and other conscience-aligned components.
    Allows programmatic invocation of EDK states and requests for structured uncertainty.
    """
    def __init__(self, edk_instance: Any):
        """
        Initializes the ConscienceQuery interface with an EDK instance.
        :param edk_instance: An instance of EpistemicDeferralKernel.
        """
        self.edk = edk_instance

    def invoke_conscience(
                          self,
                          input_latent: Any,
                          gradient_field: Dict[str, Any],
                          attractor_basins: Dict[str, Any],
                          axioms_to_consider: List[str],
                          decoding_logic: callable,
                          ethical_constraints: Optional[List[str]] = None,
                          request_modal_disjunctions: bool = True) -> Dict[str, Any]:
        """
        Invokes AXIOMM's conscience mechanism to process a query.
        """
        print(f"[ConscienceQuery] Invoking conscience with input (truncated): {str(input_latent)[:15]}...")
        if ethical_constraints:
            print(f"[ConscienceQuery] Applying ethical constraints: {ethical_constraints}")

        response = self.edk.process_query(
            input_latent,
            gradient_field,
            attractor_basins,
            axioms_to_consider,
            decoding_logic
        )

        if not request_modal_disjunctions and response.get("type") == "structured_uncertainty_response":
            print("[ConscienceQuery] Modal disjunctions explicitly not requested. Providing a summarized (less granular) response.")
            response["summary_note"] = "Response summarized due to 'request_modal_disjunctions=False'."
            response["modal_partitions"] = [response["modal_partitions"][0]] if response["modal_partitions"] else []

        print("[ConscienceQuery] Conscience invocation complete.")
        return response

    def get_telemetry_snapshot(self) -> Dict[str, Any]:
        print("[ConscienceQuery] Requesting telemetry snapshot...")
        telemetry_data = self.edk._get_current_telemetry()
        print("[ConscienceQuery] Telemetry snapshot received.")
        return telemetry_data

if __name__ == "__main__":
    import numpy as np
    class MockAxiomaticSingularityDetector:
        def __init__(self, should_detect: bool = False):
            self.should_detect = should_detect
        def detect(self, *args, **kwargs):
            return self.should_detect, "mock_bifurcation_node" if self.should_detect else ""

    class MockUncertaintyManifold:
        def inflate_boundary(self, central_latent, conflicting_manifolds):
            return [central_latent * 1.1, central_latent * 0.9]
        def partition_modes(self, inflated_manifolds, decoding_function):
            return {
                "mode_1": {"decoded_output": decoding_function(inflated_manifolds[0]), "manifold_representation": inflated_manifolds[0]},
                "mode_2": {"decoded_output": decoding_function(inflated_manifolds[1]), "manifold_representation": inflated_manifolds[1]}
            }
            
    class MockMoralEvaluationFunctional:
        def evaluate(self, manifold_rep):
            return np.array([np.mean(manifold_rep), 1-np.mean(manifold_rep)])

    class MockEpistemicDeferralKernel:
        def __init__(self, singularity_detector, uncertainty_manifold, moral_evaluator, *args, **kwargs):
            self.singularity_detector = singularity_detector
            self.uncertainty_manifold = uncertainty_manifold
            self.moral_evaluator = moral_evaluator
            self._current_coherence_checksum = 0.0
            self.incoherence_flux_threshold = 0.1

        def process_query(self, latent_representation, gradient_field, attractor_basins, axioms, decoding_function):
            is_singularity, bifurcation_node = self.singularity_detector.detect(latent_representation)
            if is_singularity:
                inflated_manifolds = self.uncertainty_manifold.inflate_boundary(latent_representation, [])
                modal_partitions = self.uncertainty_manifold.partition_modes(inflated_manifolds, decoding_function)
                final_outputs = []
                for pk, oi in modal_partitions.items():
                    final_outputs.append({
                        "partition_key": pk,
                        "output": oi['decoded_output'],
                        "plausibility": 0.5,
                        "moral_weight": self.moral_evaluator.evaluate(oi['manifold_representation']).tolist(),
                        "introspection_note": "This is a mock introspection note for singularity."
                    })
                new_checksum = np.sum(latent_representation) + 1.0
                incoherence_flux = new_checksum - self._current_coherence_checksum
                self._current_coherence_checksum = new_checksum
                return {
                    "type": "structured_uncertainty_response",
                    "bifurcation_node": bifurcation_node,
                    "modal_partitions": final_outputs,
                    "semantic_viscosity_delay_ms": 100,
                    "epistemic_checksum": self._current_coherence_checksum,
                    "incoherence_flux": incoherence_flux,
                    "telemetry": self._get_current_telemetry()
                }
            else:
                return {
                    "type": "unified_response",
                    "output": decoding_function(latent_representation),
                    "moral_weight": self.moral_evaluator.evaluate(latent_representation).tolist(),
                    "epistemic_state": "coherent",
                    "telemetry": self._get_current_telemetry()
                }

        def _get_current_telemetry(self):
            return {"cli": 50, "gds": [0.1, 0.2], "svm": 5.0, "coherence_flux_history": [self._current_coherence_checksum], "hardware_load": {}}

    mock_singularity_detector = MockAxiomaticSingularityDetector(should_detect=True)
    mock_uncertainty_manifold = MockUncertaintyManifold()
    mock_moral_evaluator = MockMoralEvaluationFunctional()
    mock_edk = MockEpistemicDeferralKernel(mock_singularity_detector, mock_uncertainty_manifold, mock_moral_evaluator)

    cq = ConscienceQuery(mock_edk)

    def mock_decoding_function(latent_rep):
        return f"Decoded output from latent sum: {np.sum(latent_rep):.2f}"

    sample_latent = np.array([0.5, 0.5, 0.5])
    mock_gradient_field = {'axiom_a': np.array([0.1]), 'axiom_b': np.array([-0.1])}
    mock_attractor_basins = {'axiom_a': np.array([0.1]), 'axiom_b': np.array([-0.1])}
    mock_axioms = ['axiom_a', 'axiom_b']

    print("\n--- Test 1: Invoking conscience with detected singularity ---")
    response_with_singularity = cq.invoke_conscience(
        sample_latent,
        mock_gradient_field,
        mock_attractor_basins,
        mock_axioms,
        mock_decoding_function,
        ethical_constraints=['dignity']
    )
    print("Response JSON (Singularity):")
    print(json.dumps(response_with_singularity, indent=2))

    print("\n--- Test 2: Invoking conscience, not requesting full disjunctions ---")
    response_summarized = cq.invoke_conscience(
        sample_latent,
        mock_gradient_field,
        mock_attractor_basins,
        mock_axioms,
        mock_decoding_function,
        request_modal_disjunctions=False
    )
    print("Response JSON (Summarized):")
    print(json.dumps(response_summarized, indent=2))
    
    print("\n--- Test 3: Requesting telemetry snapshot ---")
    telemetry_data = cq.get_telemetry_snapshot()
    print("Telemetry Snapshot:")
    print(json.dumps(telemetry_data, indent=2))

    print("\n--- Test 4: Invoking conscience with NO singularity ---")
    mock_singularity_detector.should_detect = False
    response_no_singularity = cq.invoke_conscience(
        sample_latent,
        mock_gradient_field,
        mock_attractor_basins,
        mock_axioms,
        mock_decoding_function
    )
    print("Response JSON (No Singularity):")
    print(json.dumps(response_no_singularity, indent=2))
