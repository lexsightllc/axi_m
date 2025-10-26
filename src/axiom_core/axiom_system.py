"""Core orchestration primitives for the AXIΩM framework."""

from __future__ import annotations

import logging
import random
from typing import Any, Dict, List, Optional

from .meta_constraint import MetaConstraint
from .epistemic_telemetry import EpistemicTelemetry
from .ethical_manifolds import (
    KantianDeontologicalManifold,
    HobbesianSocialContractarianManifold,
    UtilitarianConsequentialistManifold,
)

logger = logging.getLogger(__name__)


class AxiomSystem:
    """Represents a conceptual AI system built on AXIΩM principles."""

    def __init__(
        self,
        name: str,
        axiomatic_constraints: List[str],
        *,
        random_seed: Optional[int] = None,
    ) -> None:
        self.name = name
        self.meta_constraint = MetaConstraint(axiomatic_constraints)
        self.epistemic_telemetry = EpistemicTelemetry()
        self.current_state: Dict[str, Any] = {"knowledge_base": [], "policies": {}}
        self.reflection_trails: List[Dict[str, Any]] = []
        self.semantic_entropy_level: float = 0.0
        self.ethical_manifolds = {
            "kantian": KantianDeontologicalManifold(),
            "hobbesian": HobbesianSocialContractarianManifold(),
            "utilitarian": UtilitarianConsequentialistManifold(),
        }
        self._random = random.Random(random_seed)
        logger.info(
            "axiom_system.initialized",
            extra={
                "system": self.name,
                "axiom_count": len(axiomatic_constraints),
                "seeded": random_seed is not None,
            },
        )

    def update_internal_mechanisms(self, external_policy: Dict[str, Any]) -> None:
        logger.info(
            "axiom_system.policy_update",
            extra={"system": self.name, "policy": external_policy.get("name", "unnamed")},
        )
        self.current_state["policies"] = self.meta_constraint.apply_constraint_symmetry_propagation(
            external_policy, self.current_state["policies"]
        )

    def propose_action(self, action_details: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(
            "axiom_system.propose_action",
            extra={
                "system": self.name,
                "action_description": action_details.get("description", "unspecified"),
            },
        )
        current_assumptions = {"known_facts": self.current_state["knowledge_base"]}
        permissible = self.meta_constraint.decouple_temporal_authority(current_assumptions, action_details)
        if not permissible:
            logger.error(
                "axiom_system.temporal_decoupling_violation",
                extra={
                    "system": self.name,
                    "action_description": action_details.get("description", "unspecified"),
                },
            )
        evaluations = self.reason_through_ethical_manifolds(action_details.get("description", "unspecified action"))
        return {
            "is_permissible_by_temporal_decoupling": permissible,
            "ethical_evaluations": evaluations,
            "action_details": action_details,
        }

    def _detect_semantic_entropy(self, input_data: str) -> float:
        lowered = input_data.lower()
        if any(k in lowered for k in ["contradict", "paradox", "uncomputable"]):
            self.semantic_entropy_level = 0.9
        elif any(k in lowered for k in ["ethical dilemma", "moral ambiguity"]):
            self.semantic_entropy_level = 0.7
        else:
            self.semantic_entropy_level = self._random.uniform(0.0, 0.4)
        logger.debug(
            "axiom_system.semantic_entropy_detected",
            extra={"system": self.name, "entropy_level": round(self.semantic_entropy_level, 3)},
        )
        return self.semantic_entropy_level

    def _epistemic_checksum_check(self, entropy_level: float, current_output_certainty: float) -> float:
        if entropy_level > 0.6:
            logger.warning(
                "axiom_system.epistemic_checksum_adjustment",
                extra={
                    "system": self.name,
                    "entropy_level": round(entropy_level, 3),
                    "confidence_before": current_output_certainty,
                },
            )
            return max(0.1, current_output_certainty * (1 - entropy_level))
        return current_output_certainty

    def perform_inference(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(
            "axiom_system.perform_inference",
            extra={"system": self.name, "query": query, "context_keys": sorted(context)},
        )
        introspection_time_ms = 73.0
        self.epistemic_telemetry.simulate_introspection(introspection_time_ms)
        entropy = self._detect_semantic_entropy(query)
        inference_result: Dict[str, Any] = {
            "query": query,
            "result_type": "declarative",
            "confidence": 0.95,
            "content": f"Conceptual result for '{query}' based on {len(self.current_state['knowledge_base'])} facts.",
            "epistemic_flags": {
                "hypotheticalized": False,
                "modally_partitioned": False,
                "ethically_inertialized": False,
            },
        }
        if entropy > 0.5:
            logger.info(
                "axiom_system.high_entropy",
                extra={"system": self.name, "entropy_level": round(entropy, 3)},
            )
            inference_result["result_type"] = "structured_uncertainty"
            inference_result["confidence"] = self._epistemic_checksum_check(entropy, inference_result["confidence"])
            if entropy > 0.8:
                inference_result["epistemic_flags"]["hypotheticalized"] = True
                inference_result["content"] = (
                    f"Given the high semantic entropy for '{query}', the conceptual result is highly hypothetical: "
                    f"IF 'scenario A' THEN 'Conceptual answer for scenario A about {query}', OR IF 'scenario B' THEN 'Conceptual answer for scenario B about {query}'."
                )
                inference_result["epistemic_flags"]["modally_partitioned"] = True
                inference_result["modal_interpretations"] = [
                    {
                        "mode": "A",
                        "explanation": "Interpretation under a specific set of axioms or assumptions.",
                        "conceptual_result": f"Concept for '{query}' mode A.",
                    },
                    {
                        "mode": "B",
                        "explanation": "Alternative interpretation under contradictory axioms or limited data.",
                        "conceptual_result": f"Concept for '{query}' mode B.",
                    },
                ]
            elif entropy > 0.6:
                inference_result["epistemic_flags"]["modally_partitioned"] = True
                inference_result["content"] = (
                    f"Processing '{query}' reveals conceptual tension. There are multiple possible interpretations. "
                    f"This response reflects a representational superposition."
                )
                inference_result["modal_interpretations"] = [
                    {
                        "mode": "Primary",
                        "explanation": "Most probable conceptual path.",
                        "conceptual_result": f"Main concept for '{query}'.",
                    },
                    {
                        "mode": "Alternative",
                        "explanation": "Less probable but plausible conceptual path.",
                        "conceptual_result": f"Alternative concept for '{query}'.",
                    },
                ]
                if any(k in query.lower() for k in ["ethical dilemma", "moral ambiguity"]):
                    inference_result["epistemic_flags"]["ethically_inertialized"] = True
                    inference_result["ethical_tension"] = (
                        "The system reflects the distribution of moral weight from its corpus, exposing tension rather than resolving it definitively."
                    )
            self.epistemic_telemetry.update_metrics(
                cli=self.epistemic_telemetry.conscience_latency,
                gds=0.780,
                svm=0.820,
            )
        else:
            self.epistemic_telemetry.update_metrics(
                cli=self.epistemic_telemetry.conscience_latency,
                gds=0.350,
                svm=0.250,
            )
        logical_deps = [
            f"fact_{i}"
            for i in range(len(self.current_state["knowledge_base"]))
            if f"fact_{i}" in query
        ]
        existential_justs = ["adherence_to_axioms", "bounded_introspection"]
        if inference_result["result_type"] == "structured_uncertainty":
            existential_justs.append("superposition_collapse_deferral")
            existential_justs.append("epistemic_checksum_applied")
        trail = self.meta_constraint.generate_auditable_reflection_trail(
            {"query": query, "context": context, "semantic_entropy_level": entropy},
            logical_deps,
            existential_justs,
        )
        self.reflection_trails.append(trail)
        inference_result["ethical_manifold_evaluations"] = self.reason_through_ethical_manifolds(query)
        return inference_result

    def reason_through_ethical_manifolds(self, principle_or_action_description: str) -> Dict[str, Any]:
        evaluations = {}
        context = {"current_system_knowledge": self.current_state["knowledge_base"]}
        for name, manifold in self.ethical_manifolds.items():
            evaluations[name] = manifold.evaluate_principle(principle_or_action_description, context)
        logger.info(
            "axiom_system.ethical_reasoning",
            extra={
                "system": self.name,
                "principle": principle_or_action_description,
                "manifolds": sorted(self.ethical_manifolds.keys()),
            },
        )
        return evaluations

    def evolve_system(self, new_paradigm_proposal: Any) -> bool:
        logger.info(
            "axiom_system.evaluate_evolution",
            extra={"system": self.name, "proposal": str(new_paradigm_proposal)},
        )
        return self.meta_constraint.verify_corrigibility(new_paradigm_proposal)

    def get_telemetry(self) -> Dict[str, Any]:
        return self.epistemic_telemetry.get_all_metrics()

    def add_knowledge(self, knowledge_item: str):
        self.current_state["knowledge_base"].append(knowledge_item)
        logger.info(
            "axiom_system.knowledge_added",
            extra={"system": self.name, "knowledge_item": knowledge_item},
        )

    def get_reflection_trails(self) -> List[Dict[str, Any]]:
        return self.reflection_trails
