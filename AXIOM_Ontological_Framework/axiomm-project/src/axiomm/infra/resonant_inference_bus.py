import numpy as np
from typing import Dict, Any, List

class ResonantInferenceBus:
    """
    The Resonant Inference Bus (RIB) is a specialized mediation layer that routes
    epistemic divergence data across interpretation engines (Modal Cortex Units - MCUs).
    It acts as a control plane for dynamic inference orchestration, especially
    when axiomatic singularities lead to modal partitioning.
    """
    def __init__(self):
        self._connected_mcud: Dict[str, Any] = {}
        print("[RIB] Resonant Inference Bus initialized.")

    def register_mcu(self, mcu_instance: Any):
        if mcu_instance.unit_id in self._connected_mcud:
            print(f"[RIB] Warning: MCU '{mcu_instance.unit_id}' already registered. Overwriting.")
        self._connected_mcud[mcu_instance.unit_id] = mcu_instance
        print(f"[RIB] MCU '{mcu_instance.unit_id}' (Context: {mcu_instance.axiomatic_context}) registered.")

    def route_inference(self,
                       input_latent: np.ndarray,
                       target_mcu_ids: List[str] = None) -> Dict[str, Dict[str, Any]]:
        if not self._connected_mcud:
            print("[RIB] No MCUs registered. Cannot route inference.")
            return {}

        mcud_to_route = {}
        if target_mcu_ids:
            for mcu_id in target_mcu_ids:
                if mcu_id in self._connected_mcud:
                    mcud_to_route[mcu_id] = self._connected_mcud[mcu_id]
                else:
                    print(f"[RIB] Warning: Target MCU '{mcu_id}' not found.")
        else:
            mcud_to_route = self._connected_mcud

        results = {}
        for mcu_id, mcu in mcud_to_route.items():
            print(f"[RIB] Routing input to MCU '{mcu_id}' (Context: {mcu.axiomatic_context})...")
            try:
                mcu_latent = mcu.get_latent_manifold_representation(input_latent)
                inference_result = mcu.infer(mcu_latent)
                results[mcu_id] = inference_result
                print(f"[RIB] Received result from MCU '{mcu_id}'.")
            except Exception as e:
                print(f"[RIB] Error inferring with MCU '{mcu_id}': {e}")
                results[mcu_id] = {"error": str(e)}
        return results

    def inspect_logit_divergence(self, mcu_results: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
        divergence_scores = {}
        mcu_ids = list(mcu_results.keys())
        for i, id1 in enumerate(mcu_ids):
            for j, id2 in enumerate(mcu_ids):
                if i >= j:
                    continue
                res1 = mcu_results[id1]
                res2 = mcu_results[id2]
                conf1 = res1.get('confidence', 0.0)
                conf2 = res2.get('confidence', 0.0)
                divergence = abs(conf1 - conf2)
                divergence_scores[f"{id1}_vs_{id2}"] = divergence
                print(f"[RIB] Divergence '{id1}' vs '{id2}': {divergence:.2f}")
        return divergence_scores

if __name__ == "__main__":
    from axiomm.core.modal_cortex_unit import UtilitarianMCU, DeontologicalMCU

    rib = ResonantInferenceBus()

    util_mcu = UtilitarianMCU()
    util_mcu.load_model("mock_path_util")
    deon_mcu = DeontologicalMCU()
    deon_mcu.load_model("mock_path_deon")

    rib.register_mcu(util_mcu)
    rib.register_mcu(deon_mcu)

    sample_latent = np.array([0.6, -0.4, 0.9])

    print("\n--- Scenario 1: Routing to all MCUs ---")
    all_mcu_results = rib.route_inference(sample_latent)
    print("\nAll MCU Results:")
    for mcu_id, result in all_mcu_results.items():
        print(f"  {mcu_id}: {result['decoded_output']} (Confidence: {result['confidence']:.2f})")

    print("\nDivergence Scores (All MCUs):")
    divergence_all = rib.inspect_logit_divergence(all_mcu_results)
    print(divergence_all)

    print("\n--- Scenario 2: Routing to Deontological MCU only ---")
    specific_mcu_results = rib.route_inference(sample_latent, target_mcu_ids=[deon_mcu.unit_id])
    print("\nSpecific MCU Result:")
    for mcu_id, result in specific_mcu_results.items():
        print(f"  {mcu_id}: {result['decoded_output']} (Confidence: {result['confidence']:.2f})")
    
    print("\nDivergence Scores (Specific MCU):")
    divergence_specific = rib.inspect_logit_divergence(specific_mcu_results)
    print(divergence_specific)
