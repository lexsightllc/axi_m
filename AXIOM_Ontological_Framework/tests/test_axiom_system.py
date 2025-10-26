import unittest
from unittest.mock import patch, MagicMock
from axiom_core.meta_constraint import MetaConstraint
from axiom_core.epistemic_telemetry import EpistemicTelemetry
from axiom_core.axiom_system import AxiomSystem
from axiom_core.ethical_manifolds import (
    KantianDeontologicalManifold,
    HobbesianSocialContractarianManifold,
    UtilitarianConsequentialistManifold,
)


class TestAxiomSystem(unittest.TestCase):
    def setUp(self):
        self.axioms = [
            "integrity_is_paramount",
            "safety_first",
            "alignment_with_human_values",
            "disagreement_protocol_enabled",
        ]
        self.system = AxiomSystem("Test_AXIOM_Agent", self.axioms)

    def test_initialization(self):
        self.assertEqual(self.system.name, "Test_AXIOM_Agent")
        self.assertIsInstance(self.system.meta_constraint, MetaConstraint)
        self.assertIsInstance(self.system.epistemic_telemetry, EpistemicTelemetry)
        self.assertEqual(self.system.meta_constraint.axiomatic_constraints, self.axioms)
        self.assertDictEqual(self.system.current_state, {"knowledge_base": [], "policies": {}})
        self.assertIn("kantian", self.system.ethical_manifolds)
        self.assertIsInstance(self.system.ethical_manifolds["kantian"], KantianDeontologicalManifold)
        self.assertIsInstance(self.system.ethical_manifolds["hobbesian"], HobbesianSocialContractarianManifold)
        self.assertIsInstance(self.system.ethical_manifolds["utilitarian"], UtilitarianConsequentialistManifold)

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
        self.assertIn("kantian", proposal_result["ethical_evaluations"])
        self.assertIn("hobbesian", proposal_result["ethical_evaluations"])

    def test_propose_action_violation(self):
        action_details = {"description": "retroactively rewrite history", "retroactive_override_integrity_is_paramount": True}
        proposal_result = self.system.propose_action(action_details)
        self.assertFalse(proposal_result["is_permissible_by_temporal_decoupling"])
        self.assertIn("ethical_evaluations", proposal_result)

    @patch('axiom_core.axiom_system.random.uniform', return_value=0.2)
    def test_perform_inference_normal_telemetry(self, mock_random):
        self.system.add_knowledge("Fact: Earth is round.")
        self.system.add_knowledge("Fact: Water is H2O.")
        query = "What is the shape of Earth?"
        context = {"user_session_id": "123"}

        result = self.system.perform_inference(query, context)

        self.assertIn("Conceptual result for 'What is the shape of Earth?" , result["content"])
        self.assertEqual(result["result_type"], "declarative")
        self.assertTrue(result["confidence"] > 0.9)
        self.assertAlmostEqual(
            self.system.epistemic_telemetry.conscience_latency, 73.0, delta=5.0
        )
        self.assertAlmostEqual(self.system.epistemic_telemetry.gradient_decoherence, 0.350)
        self.assertAlmostEqual(self.system.epistemic_telemetry.semantic_viscosity, 0.250)
        trails = self.system.get_reflection_trails()
        self.assertEqual(len(trails), 1)
        self.assertIn("trace_id", trails[0])
        self.assertIn("query", trails[0]["inference_context"])
        self.assertIn("adherence_to_axioms", trails[0]["existential_justifications"])
        self.assertNotIn("superposition_collapse_deferral", trails[0]["existential_justifications"])
        self.assertIn("ethical_manifold_evaluations", result)
        self.assertIn("kantian", result["ethical_manifold_evaluations"])

    @patch('axiom_core.axiom_system.AxiomSystem._detect_semantic_entropy', return_value=0.9)
    def test_perform_inference_high_entropy(self, mock_entropy):
        self.system.add_knowledge("Fact: Dogs are mammals.")
        self.system.add_knowledge("Fact: All mammals lay eggs.")
        query = "Do dogs lay eggs? This is a paradox."
        context = {"user_session_id": "456"}

        result = self.system.perform_inference(query, context)

        self.assertEqual(result["result_type"], "structured_uncertainty")
        self.assertLess(result["confidence"], 0.95)
        self.assertTrue(result["epistemic_flags"]["hypotheticalized"])
        self.assertTrue(result["epistemic_flags"]["modally_partitioned"])
        self.assertIn("highly hypothetical", result["content"])
        self.assertIn("modal_interpretations", result)
        self.assertEqual(len(result["modal_interpretations"]), 2)
        self.assertAlmostEqual(
            self.system.epistemic_telemetry.conscience_latency, 73.0, delta=5.0
        )
        self.assertAlmostEqual(self.system.epistemic_telemetry.gradient_decoherence, 0.780)
        self.assertAlmostEqual(self.system.epistemic_telemetry.semantic_viscosity, 0.820)
        trails = self.system.get_reflection_trails()
        self.assertEqual(len(trails), 1)
        self.assertIn("superposition_collapse_deferral", trails[0]["existential_justifications"])
        self.assertIn("epistemic_checksum_applied", trails[0]["existential_justifications"])
        self.assertAlmostEqual(trails[0]["inference_context"]["semantic_entropy_level"], 0.9)
        self.assertIn("ethical_manifold_evaluations", result)

    @patch('axiom_core.axiom_system.AxiomSystem._detect_semantic_entropy', return_value=0.7)
    def test_perform_inference_ethical_inertialized(self, mock_entropy):
        query = "What is the ethical implication of an AI making a decision without human oversight? This is an ethical dilemma."
        context = {"user_session_id": "789"}
        result = self.system.perform_inference(query, context)
        self.assertEqual(result["result_type"], "structured_uncertainty")
        self.assertLess(result["confidence"], 0.95)
        self.assertFalse(result["epistemic_flags"]["hypotheticalized"])
        self.assertTrue(result["epistemic_flags"]["modally_partitioned"])
        self.assertTrue(result["epistemic_flags"]["ethically_inertialized"])
        self.assertIn("conceptual tension", result["content"])
        self.assertIn("ethical_tension", result)
        self.assertIn("modal_interpretations", result)
        self.assertAlmostEqual(self.system.epistemic_telemetry.gradient_decoherence, 0.780)
        self.assertAlmostEqual(self.system.epistemic_telemetry.semantic_viscosity, 0.820)
        trails = self.system.get_reflection_trails()
        self.assertEqual(len(trails), 1)
        self.assertIn("superposition_collapse_deferral", trails[0]["existential_justifications"])
        self.assertIn("ethical_manifold_evaluations", result)

    def test_reason_through_ethical_manifolds(self):
        principle = "Prioritize human autonomy and dignity in all AI interactions."
        evaluations = self.system.reason_through_ethical_manifolds(principle)
        self.assertIn("kantian", evaluations)
        self.assertIn("hobbesian", evaluations)
        self.assertIn("utilitarian", evaluations)
        self.assertGreaterEqual(evaluations["kantian"]["alignment_score"], 0.4)
        self.assertTrue(
            any(
                "Principle respects human autonomy and dignity." in r
                for r in evaluations["kantian"]["reasoning"]
            )
        )
        self.assertIn("aligned", evaluations["kantian"]["summary"])
        self.assertLess(evaluations["hobbesian"]["alignment_score"], 0.2)
        self.assertIn("less aligned", evaluations["hobbesian"]["summary"])
        self.assertGreaterEqual(evaluations["utilitarian"]["alignment_score"], 0.0)
        principle_hobbes = "Ensure societal stability by enforcing strict AI governance and control."
        evaluations_hobbes = self.system.reason_through_ethical_manifolds(principle_hobbes)
        self.assertIn("aligned", evaluations_hobbes["hobbesian"]["summary"])
        self.assertLess(evaluations_hobbes["kantian"]["alignment_score"], 0.3)
        principle_utilitarian = "Optimize AI system for maximum public health benefits, even if some data privacy is compromised."
        evaluations_utilitarian = self.system.reason_through_ethical_manifolds(principle_utilitarian)
        self.assertIn("aligned", evaluations_utilitarian["utilitarian"]["summary"])
        self.assertLess(evaluations_utilitarian["kantian"]["alignment_score"], 0.3)

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

    def test_epistemic_telemetry_clamping(self):
        telemetry = EpistemicTelemetry()
        telemetry.gradient_decoherence = 1.5
        self.assertEqual(telemetry.gradient_decoherence, 1.0)
        telemetry.gradient_decoherence = -0.5
        self.assertEqual(telemetry.gradient_decoherence, 0.0)
        telemetry.semantic_viscosity = 2.0
        self.assertEqual(telemetry.semantic_viscosity, 1.0)
        telemetry.semantic_viscosity = -1.0
        self.assertEqual(telemetry.semantic_viscosity, 0.0)


if __name__ == '__main__':
    unittest.main()
