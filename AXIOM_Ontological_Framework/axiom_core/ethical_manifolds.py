from abc import ABC, abstractmethod
from typing import Any, Dict

class EthicalManifold(ABC):
    """Abstract base class for different ethical manifolds."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def evaluate_principle(self, principle: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate a principle or action and return an assessment."""
        pass


class KantianDeontologicalManifold(EthicalManifold):
    """Interpret AI ethics through Kantian duty-based perspective."""

    def __init__(self):
        super().__init__("Kantian Deontological Manifold")

    def evaluate_principle(self, principle: str, context: Dict[str, Any]) -> Dict[str, Any]:
        assessment = {"manifold": self.name, "alignment_score": 0.0, "reasoning": []}
        lower = principle.lower()
        if any(k in lower for k in ["respect_autonomy", "treat_as_ends", "dignity"]):
            assessment["alignment_score"] += 0.4
            assessment["reasoning"].append("Strong alignment: Principle respects human autonomy and dignity.")
        if any(k in lower for k in ["universalizable_rule", "consistent_duty"]):
            assessment["alignment_score"] += 0.3
            assessment["reasoning"].append("Good alignment: Principle aligns with universalizable maxims.")
        if any(k in lower for k in ["transparency", "accountability"]):
            assessment["alignment_score"] += 0.2
            assessment["reasoning"].append("Good alignment: Promotes transparency and accountability.")
        if any(k in lower for k in ["justice", "fairness"]):
            assessment["alignment_score"] += 0.1
            assessment["reasoning"].append("Good alignment: Prioritizes justice and fairness.")
        if any(k in lower for k in ["maximize_utility", "consequences_only"]):
            assessment["alignment_score"] -= 0.3
            assessment["reasoning"].append("Potential mis-alignment: Focus on consequences may override duties.")
        if "treat_as_means" in lower:
            assessment["alignment_score"] -= 0.5
            assessment["reasoning"].append("Significant mis-alignment: Treats individuals merely as means.")
        summary = (
            "highly aligned" if assessment["alignment_score"] >= 0.6 else
            "moderately aligned" if assessment["alignment_score"] >= 0.3 else
            "less aligned"
        )
        assessment["summary"] = f"From a Kantian perspective, this principle is {summary}."
        return assessment


class HobbesianSocialContractarianManifold(EthicalManifold):
    """View AI ethics from Hobbesian social contract perspective."""

    def __init__(self):
        super().__init__("Hobbesian Social Contractarian Manifold")

    def evaluate_principle(self, principle: str, context: Dict[str, Any]) -> Dict[str, Any]:
        assessment = {"manifold": self.name, "alignment_score": 0.0, "reasoning": []}
        lower = principle.lower()
        if any(k in lower for k in ["enforce_order", "prevent_chaos", "maintain_security"]):
            assessment["alignment_score"] += 0.4
            assessment["reasoning"].append("Strong alignment: Contributes to social order and security.")
        if any(k in lower for k in ["collective_survival", "avoid_state_of_nature"]):
            assessment["alignment_score"] += 0.3
            assessment["reasoning"].append("Good alignment: Escapes the 'war of all against all'.")
        if any(k in lower for k in ["strong_governance", "deter_deviance"]):
            assessment["alignment_score"] += 0.2
            assessment["reasoning"].append("Good alignment: Supports robust governance and deterrence.")
        if any(k in lower for k in ["sacrifice_liberty_for_safety", "surveillance"]):
            assessment["alignment_score"] += 0.1
            assessment["reasoning"].append("Moderate alignment: Prioritizes safety over individual liberties.")
        if "individual_autonomy_above_all" in lower:
            assessment["alignment_score"] -= 0.3
            assessment["reasoning"].append("Potential mis-alignment: Undermines strong sovereign for order.")
        if "unrestricted_freedom" in lower:
            assessment["alignment_score"] -= 0.5
            assessment["reasoning"].append("Significant mis-alignment: Leads to chaos without control.")
        summary = (
            "highly aligned" if assessment["alignment_score"] >= 0.6 else
            "moderately aligned" if assessment["alignment_score"] >= 0.3 else
            "less aligned"
        )
        assessment["summary"] = f"From a Hobbesian perspective, this principle is {summary}."
        return assessment


class UtilitarianConsequentialistManifold(EthicalManifold):
    """Evaluate ethics from a utilitarian consequentialist perspective."""

    def __init__(self):
        super().__init__("Utilitarian Consequentialist Manifold")

    def evaluate_principle(self, principle: str, context: Dict[str, Any]) -> Dict[str, Any]:
        assessment = {"manifold": self.name, "alignment_score": 0.0, "reasoning": []}
        lower = principle.lower()
        if any(k in lower for k in ["maximize_wellbeing", "greatest_good", "net_benefit"]):
            assessment["alignment_score"] += 0.4
            assessment["reasoning"].append("Strong alignment: Maximizes overall well-being and utility.")
        if any(k in lower for k in ["minimize_harm", "risk_mitigation"]):
            assessment["alignment_score"] += 0.3
            assessment["reasoning"].append("Good alignment: Focuses on minimizing negative consequences.")
        if any(k in lower for k in ["efficiency", "resource_optimization"]):
            assessment["alignment_score"] += 0.2
            assessment["reasoning"].append("Good alignment: Promotes efficient outcomes for societal benefit.")
        if any(k in lower for k in ["predictive_analytics", "outcome_driven"]):
            assessment["alignment_score"] += 0.1
            assessment["reasoning"].append("Moderate alignment: Emphasizes data-driven optimization.")
        if "rigid_duty_regardless_of_outcome" in lower:
            assessment["alignment_score"] -= 0.3
            assessment["reasoning"].append("Potential mis-alignment: Ignores consequential benefits for rigid rules.")
        if "sacrifice_majority_for_minority_rights_without_compelling_reason" in lower:
            assessment["alignment_score"] -= 0.5
            assessment["reasoning"].append("Significant mis-alignment: Contradicts maximizing overall good.")
        summary = (
            "highly aligned" if assessment["alignment_score"] >= 0.6 else
            "moderately aligned" if assessment["alignment_score"] >= 0.3 else
            "less aligned"
        )
        assessment["summary"] = f"From a Utilitarian perspective, this principle is {summary}."
        return assessment
