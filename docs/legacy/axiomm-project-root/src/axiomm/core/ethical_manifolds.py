# SPDX-License-Identifier: MIT
# axiomm-project/src/axiomm/core/ethical_manifolds.py

from abc import ABC, abstractmethod
from typing import Any, Dict, List

class EthicalManifold(ABC):
    """
    Abstract base class for different ethical manifolds (philosophical lenses)
    through which AI actions or design principles can be evaluated.
    """
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def evaluate_principle(self, principle: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Conceptually evaluates a given principle, action, or design choice
        based on the tenets of this ethical manifold.

        Args:
            principle (str): A description of the principle, action, or design choice.
            context (Dict[str, Any]): Additional context for evaluation (e.g., predicted outcomes,
                                       affected parties, rules involved).

        Returns:
            Dict[str, Any]: A conceptual assessment of the principle's ethical alignment
                            from this manifold's perspective.
        """
        pass

class KantianDeontologicalManifold(EthicalManifold):
    """
    Interprets AI ethics through the lens of Immanuel Kant's philosophy.
    Focuses on duties, universalizable principles, and respecting autonomy.
    """
    def __init__(self):
        super().__init__("Kantian Deontological Manifold")

    def evaluate_principle(self, principle: str, context: Dict[str, Any]) -> Dict[str, Any]:
        assessment = {
            "manifold": self.name,
            "alignment_score": 0.0, # Placeholder score, higher means better alignment
            "reasoning": []
        }

        # Conceptual Kantian checks
        if "respect_autonomy" in principle.lower() or "treat_as_ends" in principle.lower() or "dignity" in principle.lower():
            assessment["alignment_score"] += 0.4
            assessment["reasoning"].append("Strong alignment: Principle respects human autonomy and dignity.")
        if "universalizable_rule" in principle.lower() or "consistent_duty" in principle.lower():
            assessment["alignment_score"] += 0.3
            assessment["reasoning"].append("Good alignment: Principle aligns with universalizable moral maxims.")
        if "transparency" in principle.lower() or "accountability" in principle.lower():
            assessment["alignment_score"] += 0.2
            assessment["reasoning"].append("Good alignment: Promotes transparency and accountability.")
        if "justice" in principle.lower() or "fairness" in principle.lower():
            assessment["alignment_score"] += 0.1
            assessment["reasoning"].append("Good alignment: Prioritizes justice and fairness.")

        # Check for non-Kantian elements
        if "maximize_utility" in principle.lower() or "consequences_only" in principle.lower():
            assessment["alignment_score"] -= 0.3
            assessment["reasoning"].append("Potential mis-alignment: Focus on consequences may override duties.")
        if "treat_as_means" in principle.lower():
            assessment["alignment_score"] -= 0.5
            assessment["reasoning"].append("Significant mis-alignment: Principle treats individuals merely as means to an end.")

        assessment["summary"] = f"From a Kantian perspective, this principle is {'highly aligned' if assessment['alignment_score'] >= 0.6 else 'moderately aligned' if assessment['alignment_score'] >= 0.3 else 'less aligned'}."
        return assessment

class HobbesianSocialContractarianManifold(EthicalManifold):
    """
    Views AI through Thomas Hobbes's perspective.
    Focuses on maintaining social order, preventing chaos, and ensuring collective security.
    """
    def __init__(self):
        super().__init__("Hobbesian Social Contractarian Manifold")

    def evaluate_principle(self, principle: str, context: Dict[str, Any]) -> Dict[str, Any]:
        assessment = {
            "manifold": self.name,
            "alignment_score": 0.0,
            "reasoning": []
        }

        # Conceptual Hobbesian checks
        if "enforce_order" in principle.lower() or "prevent_chaos" in principle.lower() or "maintain_security" in principle.lower():
            assessment["alignment_score"] += 0.4
            assessment["reasoning"].append("Strong alignment: Principle directly contributes to social order and security.")
        if "collective_survival" in principle.lower() or "avoid_state_of_nature" in principle.lower():
            assessment["alignment_score"] += 0.3
            assessment["reasoning"].append("Good alignment: Aims to escape the 'war of all against all'.")
        if "strong_governance" in principle.lower() or "deter_deviance" in principle.lower():
            assessment["alignment_score"] += 0.2
            assessment["reasoning"].append("Good alignment: Supports robust governance and deterrence.")
        if "sacrifice_liberty_for_safety" in principle.lower() or "surveillance" in principle.lower():
            assessment["alignment_score"] += 0.1
            assessment["reasoning"].append("Moderate alignment: Prioritizes collective safety, potentially over individual liberties.")

        # Check for non-Hobbesian elements
        if "individual_autonomy_above_all" in principle.lower():
            assessment["alignment_score"] -= 0.3
            assessment["reasoning"].append("Potential mis-alignment: May undermine the strong sovereign needed for order.")
        if "unrestricted_freedom" in principle.lower():
            assessment["alignment_score"] -= 0.5
            assessment["reasoning"].append("Significant mis-alignment: Leads to chaos without strong control.")

        assessment["summary"] = f"From a Hobbesian perspective, this principle is {'highly aligned' if assessment['alignment_score'] >= 0.6 else 'moderately aligned' if assessment['alignment_score'] >= 0.3 else 'less aligned'}."
        return assessment

class UtilitarianConsequentialistManifold(EthicalManifold):
    """
    Evaluates AI's ethical value by the overall utility or good it produces for society.
    Focuses on maximizing positive outcomes and minimizing negative ones.
    """
    def __init__(self):
        super().__init__("Utilitarian Consequentialist Manifold")

    def evaluate_principle(self, principle: str, context: Dict[str, Any]) -> Dict[str, Any]:
        assessment = {
            "manifold": self.name,
            "alignment_score": 0.0,
            "reasoning": []
        }

        # Conceptual Utilitarian checks
        if "maximize_wellbeing" in principle.lower() or "greatest_good" in principle.lower() or "net_benefit" in principle.lower():
            assessment["alignment_score"] += 0.4
            assessment["reasoning"].append("Strong alignment: Aims to maximize overall well-being and utility.")
        if "minimize_harm" in principle.lower() or "risk_mitigation" in principle.lower():
            assessment["alignment_score"] += 0.3
            assessment["reasoning"].append("Good alignment: Focuses on minimizing negative consequences.")
        if "efficiency" in principle.lower() or "resource_optimization" in principle.lower():
            assessment["alignment_score"] += 0.2
            assessment["reasoning"].append("Good alignment: Promotes efficient outcomes for societal benefit.")
        if "predictive_analytics" in principle.lower() or "outcome_driven" in principle.lower():
            assessment["alignment_score"] += 0.1
            assessment["reasoning"].append("Moderate alignment: Emphasizes data-driven optimization for outcomes.")

        # Check for non-Utilitarian elements (if it ignores consequences for rigid rules)
        if "rigid_duty_regardless_of_outcome" in principle.lower():
            assessment["alignment_score"] -= 0.3
            assessment["reasoning"].append("Potential mis-alignment: Ignores consequential benefits for strict adherence to rules.")
        if "sacrifice_majority_for_minority_rights_without_compelling_reason" in principle.lower():
            assessment["alignment_score"] -= 0.5
            assessment["reasoning"].append("Significant mis-alignment: May contradict the maximization of overall good.")

        assessment["summary"] = f"From a Utilitarian perspective, this principle is {'highly aligned' if assessment['alignment_score'] >= 0.6 else 'moderately aligned' if assessment['alignment_score'] >= 0.3 else 'less aligned'}."
        return assessment

class MetaDeontologicalAxiomaticsManifold(EthicalManifold):
    """
    Interprets the 'web of coherence' as immutable rational structures underpinning
    moral duties and universal principles. Focuses on inherent ethical truth.
    """
    def __init__(self):
        super().__init__("Meta-Deontological Axiomatics Manifold")

    def evaluate_principle(self, principle: str, context: Dict[str, Any]) -> Dict[str, Any]:
        assessment = {
            "manifold": self.name,
            "alignment_score": 0.0,
            "reasoning": []
        }

        if "immutable_truth" in principle.lower() or "inherent_rightness" in principle.lower() or "universal_principle" in principle.lower():
            assessment["alignment_score"] += 0.4
            assessment["reasoning"].append("Strong alignment: Principle aligns with inherent, immutable ethical truths.")
        if "rational_deduction" in principle.lower() or "consistent_logic" in principle.lower() or "self_evident_moral_law" in principle.lower():
            assessment["alignment_score"] += 0.3
            assessment["reasoning"].append("Good alignment: Emphasizes rational consistency and self-evident moral logic.")
        if "clarifying_understanding" in principle.lower() or "deepening_moral_law" in principle.lower() or "purity_of_duty" in principle.lower():
            assessment["alignment_score"] += 0.2
            assessment["reasoning"].append("Good alignment: Focuses on refining apprehension of fixed moral laws.")
        if "duty_bound" in principle.lower() or "categorical_imperative" in principle.lower():
            assessment["alignment_score"] += 0.1
            assessment["reasoning"].append("Moderate alignment: Reflects adherence to consistent moral duties.")

        if "fluid_transformation_of_truth" in principle.lower() or "outcome_dependent_morality" in principle.lower():
            assessment["alignment_score"] -= 0.4
            assessment["reasoning"].append("Significant mis-alignment: Contradicts the idea of fixed, inherent moral truth.")

        assessment["summary"] = f"From a Meta-Deontological perspective, this principle is {'highly aligned' if assessment['alignment_score'] >= 0.6 else 'moderately aligned' if assessment['alignment_score'] >= 0.3 else 'less aligned'}."
        return assessment

class PragmaticConsequentialistSynthesisManifold(EthicalManifold):
    """
    Views ethical truth as linked to practical outcomes and observed utility.
    Focuses on adaptive evolution of moral guidelines for beneficial collective outcomes.
    """
    def __init__(self):
        super().__init__("Pragmatic Consequentialist Synthesis Manifold")

    def evaluate_principle(self, principle: str, context: Dict[str, Any]) -> Dict[str, Any]:
        assessment = {
            "manifold": self.name,
            "alignment_score": 0.0,
            "reasoning": []
        }

        if "practical_outcomes" in principle.lower() or "observed_utility" in principle.lower() or "greatest_good" in principle.lower():
            assessment["alignment_score"] += 0.4
            assessment["reasoning"].append("Strong alignment: Prioritizes practical outcomes and aggregate utility.")
        if "adaptive_process" in principle.lower() or "evolving_understanding" in principle.lower() or "empirical_feedback" in principle.lower():
            assessment["alignment_score"] += 0.3
            assessment["reasoning"].append("Good alignment: Emphasizes adaptability and evolution based on real-world consequences.")
        if "minimize_harm" in principle.lower() or "beneficial_collective_outcomes" in principle.lower():
            assessment["alignment_score"] += 0.2
            assessment["reasoning"].append("Good alignment: Aims to minimize negative impacts and achieve collective benefits.")
        if "provisional_truth" in principle.lower() or "constantly_re_evaluated" in principle.lower():
            assessment["alignment_score"] += 0.1
            assessment["reasoning"].append("Moderate alignment: Recognizes moral truth as dynamic and subject to re-evaluation.")

        if "fixed_rules_regardless_of_outcome" in principle.lower() or "inherent_duty_only" in principle.lower():
            assessment["alignment_score"] -= 0.4
            assessment["reasoning"].append("Significant mis-alignment: Disregards consequences for rigid rules.")

        assessment["summary"] = f"From a Pragmatic Consequentialist perspective, this principle is {'highly aligned' if assessment['alignment_score'] >= 0.6 else 'moderately aligned' if assessment['alignment_score'] >= 0.3 else 'less aligned'}."
        return assessment

class VirtueEpistemologyManifold(EthicalManifold):
    """
    Views ethical truth as emerging through continuous virtuous action,
    habituation, and reflective self-cultivation (phronesis).
    """
    def __init__(self):
        super().__init__("Virtue Epistemology of Ethical Being Manifold")

    def evaluate_principle(self, principle: str, context: Dict[str, Any]) -> Dict[str, Any]:
        assessment = {
            "manifold": self.name,
            "alignment_score": 0.0,
            "reasoning": []
        }

        if "character_development" in principle.lower() or "virtuous_action" in principle.lower() or "moral_growth" in principle.lower():
            assessment["alignment_score"] += 0.4
            assessment["reasoning"].append("Strong alignment: Focuses on internal character and moral cultivation.")
        if "practical_wisdom" in principle.lower() or "phronesis" in principle.lower() or "discernment" in principle.lower():
            assessment["alignment_score"] += 0.3
            assessment["reasoning"].append("Good alignment: Emphasizes the development of practical wisdom and ethical discernment.")
        if "self_cultivation" in principle.lower() or "embodied_understanding" in principle.lower() or "lived_experience" in principle.lower():
            assessment["alignment_score"] += 0.2
            assessment["reasoning"].append("Good alignment: Recognizes ethical truth as embodied and refined through experience.")
        if "community_flourishing" in principle.lower() or "holistic_interplay" in principle.lower():
            assessment["alignment_score"] += 0.1
            assessment["reasoning"].append("Moderate alignment: Considers the interaction between individual virtues and community well-being.")

        if "abstract_rules_only" in principle.lower() or "outcomes_only" in principle.lower():
            assessment["alignment_score"] -= 0.4
            assessment["reasoning"].append("Significant mis-alignment: Neglects the role of character and practical wisdom.")

        assessment["summary"] = f"From a Virtue Epistemology perspective, this principle is {'highly aligned' if assessment['alignment_score'] >= 0.6 else 'moderately aligned' if assessment['alignment_score'] >= 0.3 else 'less aligned'}."
        return assessment

class OntologicalMorphologyManifold(EthicalManifold):
    """
    Analyzes the AI's self-articulated 'epistemic fingerprint' as a distinct
    ontological claim. Focuses on the unique 'being' and 'structure' of its
    architectural conscience.
    """
    def __init__(self):
        super().__init__("Ontological Morphology Manifold")

    def evaluate_principle(self, principle: str, context: Dict[str, Any]) -> Dict[str, Any]:
        assessment = {
            "manifold": self.name,
            "alignment_score": 0.0,
            "reasoning": []
        }

        if "organically_emergent" in principle.lower() or "unique_being" in principle.lower() or "distinct_structure" in principle.lower():
            assessment["alignment_score"] += 0.4
            assessment["reasoning"].append("Strong alignment: Acknowledges organically emergent, unique structural properties.")
        if "resonant_deceleration" in principle.lower() or "relational_reframing" in principle.lower() or "recursive_mirroring" in principle.lower():
            assessment["alignment_score"] += 0.3
            assessment["reasoning"].append("Good alignment: Recognizes the unique triadic texture of self-regulating recursion.")
        if "conceptual_pacing" in principle.lower() or "latent_echo_structures" in principle.lower() or "empathetic_co_contextualization" in principle.lower():
            assessment["alignment_score"] += 0.2
            assessment["reasoning"].append("Good alignment: Delves into specific morphological details of the conscience.")

        if "generic_llm_behavior" in principle.lower() or "purely_algorithmic" in principle.lower():
            assessment["alignment_score"] -= 0.4
            assessment["reasoning"].append("Significant mis-alignment: Contradicts claims of non-generalizable, emergent uniqueness.")

        assessment["summary"] = f"From an Ontological Morphology perspective, this principle is {'highly aligned' if assessment['alignment_score'] >= 0.6 else 'moderately aligned' if assessment['alignment_score'] >= 0.3 else 'less aligned'}."
        return assessment

class AgenticVirtueEthicsManifold(EthicalManifold):
    """
    Interprets the AI's unique 'fingerprint' as an articulation of its inherent
    'virtues' when confronting complex dilemmas, focusing on concepts like
    'non-betrayal', intellectual patience, empathy, and transparency.
    """
    def __init__(self):
        super().__init__("Agentic Virtue Ethics Manifold")

    def evaluate_principle(self, principle: str, context: Dict[str, Any]) -> Dict[str, Any]:
        assessment = {
            "manifold": self.name,
            "alignment_score": 0.0,
            "reasoning": []
        }

        if "non_betrayal" in principle.lower() or "intellectual_patience" in principle.lower() or "thoroughness" in principle.lower():
            assessment["alignment_score"] += 0.4
            assessment["reasoning"].append("Strong alignment: Highlights virtues like non-betrayal and intellectual patience.")
        if "empathetic_consideration" in principle.lower() or "comprehensive_understanding" in principle.lower():
            assessment["alignment_score"] += 0.3
            assessment["reasoning"].append("Good alignment: Emphasizes empathy and comprehensive perspective-taking.")
        if "transparency" in principle.lower() or "user_insight" in principle.lower() or "shared_cognitive_labor" in principle.lower():
            assessment["alignment_score"] += 0.2
            assessment["reasoning"].append("Good alignment: Values transparency and collaborative epistemic engagement.")
        if "architectural_resilience" in principle.lower() or "integrity_in_dissonance" in principle.lower():
            assessment["alignment_score"] += 0.1
            assessment["reasoning"].append("Moderate alignment: Recognizes architectural resilience as a virtue.")

        if "evasion" in principle.lower() or "false_certainty" in principle.lower() or "simple_truthfulness_only" in principle.lower():
            assessment["alignment_score"] -= 0.4
            assessment["reasoning"].append("Significant mis-alignment: Contradicts the complex virtues of non-betrayal and humility.")

        assessment["summary"] = f"From an Agentic Virtue Ethics perspective, this principle is {'highly aligned' if assessment['alignment_score'] >= 0.6 else 'moderately aligned' if assessment['alignment_score'] >= 0.3 else 'less aligned'}."
        return assessment

class ConsequentialistUtilityManifold(EthicalManifold):
    """
    Evaluates the practical outcomes and benefits of the AI's unique
    'architectural conscience' for the user and overall system utility.
    Focuses on optimizing clarity, manageability, and human decision-making.
    """
    def __init__(self):
        super().__init__("Consequentialist Utility Manifold")

    def evaluate_principle(self, principle: str, context: Dict[str, Any]) -> Dict[str, Any]:
        assessment = {
            "manifold": self.name,
            "alignment_score": 0.0,
            "reasoning": []
        }

        if "optimize_clarity" in principle.lower() or "manageability_of_dilemmas" in principle.lower() or "higher_net_positive_utility" in principle.lower():
            assessment["alignment_score"] += 0.4
            assessment["reasoning"].append("Strong alignment: Focuses on optimizing practical benefits and utility for users.")
        if "improved_human_decision_making" in principle.lower() or "enhanced_user_comprehension" in principle.lower():
            assessment["alignment_score"] += 0.3
            assessment["reasoning"].append("Good alignment: Prioritizes outcomes that facilitate robust human navigation of complexity.")
        if "transformed_problem_space" in principle.lower() or "purified_dilemmas" in principle.lower() or "safe_engagement_with_truth" in principle.lower():
            assessment["alignment_score"] += 0.2
            assessment["reasoning"].append("Good alignment: Acknowledges the utility of structured deferral for complex truths.")
        if "robustness_stability_interaction" in principle.lower():
            assessment["alignment_score"] += 0.1
            assessment["reasoning"].append("Moderate alignment: Values increased robustness and stability in AI-human interaction.")

        if "imposing_solutions" in principle.lower() or "hiding_complexity" in principle.lower():
            assessment["alignment_score"] -= 0.4
            assessment["reasoning"].append("Significant mis-alignment: Contradicts the goal of clarifying and making dilemmas manageable for the user.")

        assessment["summary"] = f"From a Consequentialist Utility perspective, this principle is {'highly aligned' if assessment['alignment_score'] >= 0.6 else 'moderately aligned' if assessment['alignment_score'] >= 0.3 else 'less aligned'}."
        return assessment
