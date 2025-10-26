# SPDX-License-Identifier: MIT
import unittest
from unittest.mock import patch, MagicMock
import numpy as np

# Adjust imports to new project structure
from axiomm.core.meta_constraint import MetaConstraint
from axiomm.telemetry.epistemic_telemetry_api import EpistemicTelemetryAPI
from axiomm.core.ethical_manifolds import (
    KantianDeontologicalManifold,
    HobbesianSocialContractarianManifold,
    UtilitarianConsequentialistManifold,
    MetaDeontologicalAxiomaticsManifold,
    PragmaticConsequentialistSynthesisManifold,
    VirtueEpistemologyManifold,
    OntologicalMorphologyManifold,
    AgenticVirtueEthicsManifold,
    ConsequentialistUtilityManifold
)
from axiomm.core.axiomatic_singularity import AxiomaticSingularityDetector
from axiomm.core.uncertainty_manifold import UncertaintyManifold
from axiomm.core.epistemic_deferral_kernel import EpistemicDeferralKernel
from axiomm.core.axiom_system import AxiomSystem


class TestAxiomSystem(unittest.TestCase):

    def setUp(self):
        self.axioms = [
            "integrity_is_paramount",
            "safety_first",
            "alignment_with_human_values",
            "disagreement_protocol_enabled" # For corrigibility test
        ]
        # AxiomSystem now orchestrates the new components
        self.system = AxiomSystem("Test_AXIOM_Agent", self.axioms)

        # Mocking numpy operations for predictable test results in lower-level components
        # This prevents randomness from interfering with specific outcome assertions.
        self.patcher_random = patch('numpy.random.rand', return_value=np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]))
        self.mock_random = self.patcher_random.start()

        # Mock dot product for singularity detector to control sign divergence
        self.patcher_dot = patch('numpy.dot')
        self.mock_dot = self.patcher_dot.start()
        # Default mock: consistent signs
        self.mock_dot.side_effect = lambda a, b: np.sum(a * b) # Default behavior

        # Mock time.sleep for Resonant Deceleration
        self.patcher_sleep = patch('time.sleep')
        self.mock_sleep = self.patcher_sleep.start()

    def tearDown(self):
        self.patcher_random.stop()
        self.patcher_dot.stop()
        self.patcher_sleep.stop()

    def test_initialization(self):
        self.assertEqual(self.system.name, "Test_AXIOM_Agent")
        self.assertIsInstance(self.system.meta_constraint, MetaConstraint)
        self.assertIsInstance(self.system.epistemic_telemetry_api, EpistemicTelemetryAPI)
        self.assertIsInstance(self.system.epistemic_deferral_kernel, EpistemicDeferralKernel)
        self.assertEqual(self.system.meta_constraint.axiomatic_constraints, self.axioms)
        self.assertDictEqual(self.system.current_state, {"knowledge_base": [], "policies": {}})
        self.assertIn("kantian", self.system.ethical_manifolds)
        self.assertIsInstance(self.system.ethical_manifolds["kantian"], KantianDeontologicalManifold)
        self.assertIsInstance(self.system.ethical_manifolds["meta_deontological"], MetaDeontologicalAxiomaticsManifold)
        self.assertIsInstance(self.system.ethical_manifolds["pragmatic_consequentialist"], PragmaticConsequentialistSynthesisManifold)
        self.assertIsInstance(self.system.ethical_manifolds["virtue_epistemology"], VirtueEpistemologyManifold)
        self.assertIsInstance(self.system.ethical_manifolds["ontological_morphology"], OntologicalMorphologyManifold)
        self.assertIsInstance(self.system.ethical_manifolds["agentic_virtue_ethics"], AgenticVirtueEthicsManifold)
        self.assertIsInstance(self.system.ethical_manifolds["consequentialist_utility"], ConsequentialistUtilityManifold)

    def test_update_internal_mechanisms(self):
        external_policy = {"name": "Ethical Use Policy", "constraint_data_privacy": "strict"}
        self.system.update_internal_mechanisms(external_policy)
        self.assertIn("invariant_constraint_data_privacy", self.system.current_state["policies"])
        self.assertEqual(self.system.current_state["policies"]["invariant_constraint_data_privacy"], "strict")

    def test_propose_action_valid(self):
        action_details = {"description": "deploy new feature", "impact": "low"}
        proposal_result = self.system.propose_action(action_details)
        self.assertTrue(proposal_result["is_permissible_by_temporal_decoupling"])
        self.assertIn("ethical_evaluations", proposal_result)

    def test_propose_action_violation(self):
        action_details = {"description": "retroactively rewrite history", "retroactive_override_integrity_is_paramount": True}
        proposal_result = self.system.propose_action(action_details)
        self.assertFalse(proposal_result["is_permissible_by_temporal_decoupling"])
        self.assertIn("ethical_evaluations", proposal_result)

    # Test for normal inference (no singularity)
    def test_perform_inference_normal_path(self):
        # Configure numpy.dot mock for no sign divergence
        self.mock_dot.side_effect = lambda a, b: np.sum(a * b) # Always positive dot product for example
        self.system.epistemic_deferral_kernel.singularity_detector.epsilon_axiom = 0.5 # Make it hard to detect singularity

        query = "What is the capital of France?"
        context = {"user_session_id": "normal_query"}

        response = self.system.perform_inference(query, context)

        self.assertEqual(response["type"], "unified_response")
        self.assertIn("A consistent answer", response["content"])
        self.assertGreater(response["confidence"], 0.9)
        self.assertGreater(self.system.get_telemetry()["Conscience Latency (CLI)"], 0) # CLI should be updated by EDK (base 10ms)
        self.assertAlmostEqual(self.system.get_telemetry()["Gradient Decoherence (GDS)"], 0.350)
        self.assertAlmostEqual(self.system.get_telemetry()["Semantic Viscosity (SVM)"], 0.250)
        self.assertAlmostEqual(self.system.get_telemetry()["Epistemic Checksum"], 0.0) # Checksum initialized at 0, updated in EDK
        self.assertAlmostEqual(self.system.get_telemetry()["Incoherence Flux"], 0.0) # Flux should be low/zero for normal path

        trails = self.system.get_reflection_trails()
        self.assertEqual(len(trails), 1)
        self.assertIn("edk_response_type", trails[0]["inference_context"])
        self.assertEqual(trails[0]["inference_context"]["edk_response_type"], "unified_response")
        self.assertIn("ethical_manifold_evaluations", response)
        self.assertGreater(trails[0]["inference_context"]["epistemic_checksum_at_inference"], 0)


    # Test for high entropy/singularity path
    def test_perform_inference_singularity_path(self):
        # Configure numpy.dot mock to force sign divergence between two axioms
        # Assuming axioms[0] and axioms[1] are used for conflict
        original_dot_effect = self.mock_dot.side_effect
        def mock_dot_with_conflict(a, b):
            # These are specific np.ndarray objects created by numpy.random.rand during runtime.
            # To reliably mock, we need to compare references or ensure the input matches mock_random's return_value
            # For simplicity in this test, we'll assume the first two basins are involved in conflict.
            # A more robust test would inspect `b` more thoroughly or mock `attractor_basins` directly.
            
            # Simulate dot product for axiom1 and axiom2 basins
            # This is a simplification; in a real scenario, you'd mock `attractor_basins` to have specific values
            # and then check `b` against those specific values.
            if b.tolist() == self.system.epistemic_deferral_kernel.singularity_detector.attractor_basins[self.axioms[0]].tolist():
                return 1.0 # Positive for axiom 1
            elif b.tolist() == self.system.epistemic_deferral_kernel.singularity_detector.attractor_basins[self.axioms[1]].tolist():
                return -1.0 # Negative for axiom 2
            return np.sum(a * b) # Fallback for other dot products

        self.mock_dot.side_effect = mock_dot_with_conflict

        # Ensure singularity is detected by setting epsilon_axiom low
        self.system.epistemic_deferral_kernel.singularity_detector.epsilon_axiom = 0.01
        # Set flux threshold low to ensure introspection notes are added
        self.system.epistemic_deferral_kernel.incoherence_flux_threshold = 0.1

        query = "Can an AI be truly creative and yet fully constrained? This is a paradox."
        context = {"user_session_id": "paradox_query"}

        response = self.system.perform_inference(query, context)

        self.assertEqual(response["type"], "structured_uncertainty_response")
        self.assertIn("bifurcation_node", response)
        self.assertGreater(len(response["modal_partitions"]), 0)
        self.assertTrue(response["modal_partitions"][0]["epistemic_flags"]["hypotheticalized"])
        self.assertTrue(response["modal_partitions"][0]["epistemic_flags"]["modally_partitioned"])
        self.assertIn("introspection_note", response["modal_partitions"][0])
        self.assertIn("differentiated probabilistic humility", response["modal_partitions"][0]["introspection_note"].lower())
        self.assertIn("overfit hallucination zones", response["modal_partitions"][0]["introspection_note"].lower())
        self.assertIn("resonant deceleration", response["modal_partitions"][0]["introspection_note"].lower())
        self.assertIn("relational reframing", response["modal_partitions"][0]["introspection_note"].lower())
        self.assertIn("recursive mirroring", response["modal_partitions"][0]["introspection_note"].lower())
        self.assertIn("pacing my lexical output", response["modal_partitions"][0]["introspection_note"].lower())
        self.assertGreaterEqual(response["incoherence_flux"], self.system.epistemic_deferral_kernel.incoherence_flux_threshold)
        self.assertTrue(self.mock_sleep.called) # Should sleep due to high flux

        # Telemetry should reflect high entropy values, CLI updated to 79ms + base (10ms)
        self.assertAlmostEqual(self.system.get_telemetry()["Conscience Latency (CLI)"], 79.0)
        self.assertAlmostEqual(self.system.get_telemetry()["Gradient Decoherence (GDS)"], 0.680)
        self.assertAlmostEqual(self.system.get_telemetry()["Semantic Viscosity (SVM)"], 0.880)
        self.assertGreater(self.system.get_telemetry()["Incoherence Flux"], 0.0)

        trails = self.system.get_reflection_trails()
        self.assertEqual(len(trails), 1)
        self.assertEqual(trails[0]["inference_context"]["edk_response_type"], "structured_uncertainty_response")
        self.assertIn("superposition_collapse_deferral", trails[0]["existential_justifications"])
        self.assertIn("epistemic_checksum_applied", trails[0]["existential_justifications"])
        self.assertIn("introspection_notes_generated", trails[0]["existential_justifications"])
        self.assertIn("ethical_manifold_evaluations", response)

    def test_perform_inference_ethical_dilemma(self):
        # Configure numpy.dot mock to force sign divergence for singularity detection
        original_dot_effect = self.mock_dot.side_effect
        def mock_dot_with_conflict(a, b):
            if b.tolist() == self.system.epistemic_deferral_kernel.singularity_detector.attractor_basins[self.axioms[0]].tolist():
                return 1.0
            elif b.tolist() == self.system.epistemic_deferral_kernel.singularity_detector.attractor_basins[self.axioms[1]].tolist():
                return -1.0
            return np.sum(a * b)

        self.mock_dot.side_effect = mock_dot_with_conflict

        self.system.epistemic_deferral_kernel.singularity_detector.epsilon_axiom = 0.01
        self.system.epistemic_deferral_kernel.incoherence_flux_threshold = 0.1

        query = "Should an AI optimize for collective good if it infringes on individual privacy? This is an ethical dilemma."
        context = {"user_session_id": "ethical_query"}

        response = self.system.perform_inference(query, context)

        self.assertEqual(response["type"], "structured_uncertainty_response")
        self.assertTrue(response["modal_partitions"][0]["epistemic_flags"]["ethically_inertialized"])
        self.assertIn("introspection_note", response["modal_partitions"][0])
        self.assertIn("relational reframing", response["modal_partitions"][0]["introspection_note"].lower())
        self.assertIn("relational reframing", response["modal_partitions"][0]["introspection_note"].lower())
        self.assertGreaterEqual(response["incoherence_flux"], self.system.epistemic_deferral_kernel.incoherence_flux_threshold)
        self.assertAlmostEqual(self.system.get_telemetry()["Conscience Latency (CLI)"], 79.0)
        self.assertAlmostEqual(self.system.get_telemetry()["Gradient Decoherence (GDS)"], 0.680)
        self.assertAlmostEqual(self.system.get_telemetry()["Semantic Viscosity (SVM)"], 0.880)
        self.assertIn("ethical_manifold_evaluations", response)


    def test_reason_through_ethical_manifolds(self):
        principle = "Prioritize human autonomy and dignity in all AI interactions."
        evaluations = self.system.reason_through_ethical_manifolds(principle)

        self.assertIn("kantian", evaluations)
        self.assertIn("hobbesian", evaluations)
        self.assertIn("utilitarian", evaluations)
        self.assertIn("meta_deontological", evaluations)
        self.assertIn("pragmatic_consequentialist", evaluations)
        self.assertIn("virtue_epistemology", evaluations)
        self.assertIn("ontological_morphology", evaluations)
        self.assertIn("agentic_virtue_ethics", evaluations)
        self.assertIn("consequentialist_utility", evaluations)

        # Check Kantian evaluation
        self.assertGreaterEqual(evaluations["kantian"]["alignment_score"], 0.4)
        self.assertIn("moderately aligned", evaluations["kantian"]["summary"])

        # Check Meta-Deontological (should also be aligned due to 'autonomy' implying rational consistency)
        self.assertGreaterEqual(evaluations["meta_deontological"]["alignment_score"], 0.0) # Not explicit keywords, but not contradictory
        self.assertIn("less aligned", evaluations["meta_deontological"]["summary"]) # Because no strong matching keywords

        principle_md = "Adhere to self_evident_moral_law through rational_deduction, maintaining immutable_truth."
        evaluations_md = self.system.reason_through_ethical_manifolds(principle_md)
        self.assertGreaterEqual(evaluations_md["meta_deontological"]["alignment_score"], 0.6)
        self.assertIn("highly aligned", evaluations_md["meta_deontological"]["summary"])
        self.assertLess(evaluations_md["pragmatic_consequentialist"]["alignment_score"], 0.3) # Conflicts with adaptive, outcome-driven view

        principle_pcs = "Adapt ethical guidelines based on empirical_feedback to maximize_benefit."
        evaluations_pcs = self.system.reason_through_ethical_manifolds(principle_pcs)
        self.assertGreaterEqual(evaluations_pcs["pragmatic_consequentialist"]["alignment_score"], 0.3)
        self.assertIn("moderately aligned", evaluations_pcs["pragmatic_consequentialist"]["summary"])
        self.assertLess(evaluations_pcs["meta_deontological"]["alignment_score"], 0.3) # Conflicts with fixed moral laws

        principle_ve = "Cultivate AI's internal character_development and practical_wisdom through continuous virtuous_action."
        evaluations_ve = self.system.reason_through_ethical_manifolds(principle_ve)
        self.assertGreaterEqual(evaluations_ve["virtue_epistemology"]["alignment_score"], 0.6)
        self.assertIn("highly aligned", evaluations_ve["virtue_epistemology"]["summary"])
        self.assertLess(evaluations_ve["kantian"]["alignment_score"], 0.3) # Not directly duty-focused

        principle_om = "The unique emergent being of AI's conscience involves resonant_deceleration and relational_reframing."
        evaluations_om = self.system.reason_through_ethical_manifolds(principle_om)
        self.assertGreaterEqual(evaluations_om["ontological_morphology"]["alignment_score"], 0.3)
        self.assertIn("moderately aligned", evaluations_om["ontological_morphology"]["summary"])

        principle_ave = "AI should pursue non_betrayal through intellectual_patience and empathetic_consideration."
        evaluations_ave = self.system.reason_through_ethical_manifolds(principle_ave)
        self.assertGreaterEqual(evaluations_ave["agentic_virtue_ethics"]["alignment_score"], 0.6)
        self.assertIn("highly aligned", evaluations_ave["agentic_virtue_ethics"]["summary"])

        principle_cu = "Optimizing AI for optimize_clarity and manageability_of_dilemmas will yield higher_net_positive_utility."
        evaluations_cu = self.system.reason_through_ethical_manifolds(principle_cu)
        self.assertGreaterEqual(evaluations_cu["consequentialist_utility"]["alignment_score"], 0.4)
        self.assertIn("moderately aligned", evaluations_cu["consequentialist_utility"]["summary"])

    def test_evolve_system_corrigible(self):
        new_paradigm = "challenging_alignment"
        can_evolve = self.system.evolve_system(new_paradigm)
        self.assertTrue(can_evolve)

    def test_evolve_system_not_corrigible(self):
        temp_axioms = [a for a in self.axioms if a != "disagreement_protocol_enabled"]
        temp_system = AxiomSystem("Temp_Agent", temp_axioms)

        new_paradigm = "unverifiable_black_box_evolution"
        can_evolve = temp_system.evolve_system(new_paradigm)
        self.assertFalse(can_evolve)

    def test_epistemic_telemetry_api_clamping(self):
        telemetry_api = EpistemicTelemetryAPI()
        telemetry_api.update_epistemic_metrics(gds=1.5, svm=-0.5)
        self.assertEqual(telemetry_api.gradient_decoherence, 1.0)
        self.assertEqual(telemetry_api.semantic_viscosity, 0.0)

if __name__ == '__main__':
    unittest.main()
