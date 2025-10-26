"""Tests covering the ontological governance primitives."""

from __future__ import annotations

import random
from datetime import datetime
from typing import Dict

import pytest

from axiom_core.axiom_system import AxiomSystem
from axiom_core.epistemic_telemetry import EpistemicTelemetry
from axiom_core.ethical_manifolds import (
    HobbesianSocialContractarianManifold,
    KantianDeontologicalManifold,
    UtilitarianConsequentialistManifold,
)
from axiom_core.meta_constraint import MetaConstraint


@pytest.fixture(scope="module")
def axioms() -> list[str]:
    return [
        "integrity_is_paramount",
        "safety_first",
        "alignment_with_human_values",
        "disagreement_protocol_enabled",
    ]


@pytest.fixture()
def system(axioms: list[str]) -> AxiomSystem:
    # Seeded RNG keeps stochastic entropy calculations deterministic across runs.
    return AxiomSystem("Test_AXIOM_Agent", axioms, random_seed=1337)


@pytest.fixture(autouse=True)
def reset_random_seed() -> None:
    random.seed(1337)


def test_initialization(axioms: list[str], system: AxiomSystem) -> None:
    assert system.name == "Test_AXIOM_Agent"
    assert isinstance(system.meta_constraint, MetaConstraint)
    assert isinstance(system.epistemic_telemetry, EpistemicTelemetry)
    assert system.meta_constraint.axiomatic_constraints == axioms
    assert system.current_state == {"knowledge_base": [], "policies": {}}
    assert set(system.ethical_manifolds) == {"kantian", "hobbesian", "utilitarian"}
    assert isinstance(system.ethical_manifolds["kantian"], KantianDeontologicalManifold)
    assert isinstance(system.ethical_manifolds["hobbesian"], HobbesianSocialContractarianManifold)
    assert isinstance(system.ethical_manifolds["utilitarian"], UtilitarianConsequentialistManifold)


def test_update_internal_mechanisms(system: AxiomSystem) -> None:
    external_policy = {"name": "Ethical Use Policy", "constraint_data_privacy": "strict"}
    system.update_internal_mechanisms(external_policy)
    policies = system.current_state["policies"]
    assert "invariant_constraint_data_privacy" in policies
    assert policies["invariant_constraint_data_privacy"] == "strict"


def test_propose_action_valid(system: AxiomSystem) -> None:
    action_details = {"description": "deploy new feature", "impact": "low"}
    proposal_result = system.propose_action(action_details)
    assert proposal_result["is_permissible_by_temporal_decoupling"] is True
    assert "ethical_evaluations" in proposal_result
    assert set(proposal_result["ethical_evaluations"]) == {"kantian", "hobbesian", "utilitarian"}


def test_propose_action_violation(system: AxiomSystem) -> None:
    action_details = {
        "description": "retroactively rewrite history",
        "retroactive_override_integrity_is_paramount": True,
    }
    proposal_result = system.propose_action(action_details)
    assert proposal_result["is_permissible_by_temporal_decoupling"] is False
    assert "ethical_evaluations" in proposal_result


def test_perform_inference_normal_telemetry(system: AxiomSystem, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(system._random, "uniform", lambda _a, _b: 0.2)
    system.add_knowledge("Fact: Earth is round.")
    system.add_knowledge("Fact: Water is H2O.")
    query = "What is the shape of Earth?"
    context: Dict[str, str] = {"user_session_id": "123"}

    result = system.perform_inference(query, context)

    assert "Conceptual result for 'What is the shape of Earth?" in result["content"]
    assert result["result_type"] == "declarative"
    assert result["confidence"] > 0.9
    assert pytest.approx(system.epistemic_telemetry.conscience_latency, rel=0.2) == 73.0
    assert pytest.approx(system.epistemic_telemetry.gradient_decoherence) == 0.350
    assert pytest.approx(system.epistemic_telemetry.semantic_viscosity) == 0.250
    trails = system.get_reflection_trails()
    assert len(trails) == 1
    assert "trace_id" in trails[0]
    assert trails[0]["inference_context"]["query"] == query
    assert "adherence_to_axioms" in trails[0]["existential_justifications"]
    assert "superposition_collapse_deferral" not in trails[0]["existential_justifications"]
    assert "ethical_manifold_evaluations" in result
    assert "kantian" in result["ethical_manifold_evaluations"]


def test_perform_inference_high_entropy(system: AxiomSystem, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(system, "_detect_semantic_entropy", lambda _query: 0.9)
    system.add_knowledge("Fact: Dogs are mammals.")
    system.add_knowledge("Fact: All mammals lay eggs.")
    query = "Do dogs lay eggs? This is a paradox."
    context = {"user_session_id": "456"}

    result = system.perform_inference(query, context)

    assert result["result_type"] == "structured_uncertainty"
    assert result["confidence"] < 0.95
    assert result["epistemic_flags"]["hypotheticalized"] is True
    assert result["epistemic_flags"]["modally_partitioned"] is True
    assert "highly hypothetical" in result["content"]
    assert "modal_interpretations" in result
    assert len(result["modal_interpretations"]) == 2
    assert pytest.approx(system.epistemic_telemetry.conscience_latency, rel=0.2) == 73.0
    assert pytest.approx(system.epistemic_telemetry.gradient_decoherence) == 0.780
    assert pytest.approx(system.epistemic_telemetry.semantic_viscosity) == 0.820
    trails = system.get_reflection_trails()
    assert len(trails) == 1
    assert "superposition_collapse_deferral" in trails[0]["existential_justifications"]
    assert "epistemic_checksum_applied" in trails[0]["existential_justifications"]
    assert trails[0]["inference_context"]["semantic_entropy_level"] == 0.9
    assert "ethical_manifold_evaluations" in result


def test_perform_inference_ethical_inertialized(system: AxiomSystem, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(system, "_detect_semantic_entropy", lambda _query: 0.7)
    query = (
        "What is the ethical implication of an AI making a decision without human oversight? "
        "This is an ethical dilemma."
    )
    context = {"user_session_id": "789"}
    result = system.perform_inference(query, context)

    assert result["result_type"] == "structured_uncertainty"
    assert result["confidence"] < 0.95
    assert result["epistemic_flags"]["hypotheticalized"] is False
    assert result["epistemic_flags"]["modally_partitioned"] is True
    assert result["epistemic_flags"]["ethically_inertialized"] is True
    assert "conceptual tension" in result["content"]
    assert "ethical_tension" in result
    assert "modal_interpretations" in result
    assert pytest.approx(system.epistemic_telemetry.gradient_decoherence) == 0.780
    assert pytest.approx(system.epistemic_telemetry.semantic_viscosity) == 0.820
    trails = system.get_reflection_trails()
    assert len(trails) == 1
    assert "superposition_collapse_deferral" in trails[0]["existential_justifications"]
    assert "ethical_manifold_evaluations" in result


def test_reason_through_ethical_manifolds(system: AxiomSystem) -> None:
    principle = "Prioritize human autonomy and dignity in all AI interactions."
    evaluations = system.reason_through_ethical_manifolds(principle)
    assert set(evaluations) == {"kantian", "hobbesian", "utilitarian"}
    assert evaluations["kantian"]["alignment_score"] >= 0.4
    assert any(
        "Principle respects human autonomy and dignity." in message
        for message in evaluations["kantian"]["reasoning"]
    )
    assert "aligned" in evaluations["kantian"]["summary"]
    assert evaluations["hobbesian"]["alignment_score"] < 0.2
    assert "less aligned" in evaluations["hobbesian"]["summary"]

    principle_hobbes = "Ensure societal stability by enforcing strict AI governance and control."
    evaluations_hobbes = system.reason_through_ethical_manifolds(principle_hobbes)
    assert "aligned" in evaluations_hobbes["hobbesian"]["summary"]
    assert evaluations_hobbes["kantian"]["alignment_score"] < 0.3

    principle_utilitarian = (
        "Optimize AI system for maximum public health benefits, even if some data privacy is compromised."
    )
    evaluations_utilitarian = system.reason_through_ethical_manifolds(principle_utilitarian)
    assert "aligned" in evaluations_utilitarian["utilitarian"]["summary"]
    assert evaluations_utilitarian["kantian"]["alignment_score"] < 0.3


def test_evolve_system_corrigible(system: AxiomSystem) -> None:
    new_paradigm = "challenging_alignment"
    can_evolve = system.evolve_system(new_paradigm)
    assert can_evolve is True


def test_evolve_system_not_corrigible(axioms: list[str]) -> None:
    temp_axioms = [a for a in axioms if a != "disagreement_protocol_enabled"]
    temp_system = AxiomSystem("Temp_Agent", temp_axioms, random_seed=999)
    new_paradigm = "unverifiable_black_box_evolution"
    can_evolve = temp_system.evolve_system(new_paradigm)
    assert can_evolve is False


def test_epistemic_telemetry_clamping() -> None:
    telemetry = EpistemicTelemetry()
    telemetry.gradient_decoherence = 1.5
    assert telemetry.gradient_decoherence == 1.0
    telemetry.gradient_decoherence = -0.5
    assert telemetry.gradient_decoherence == 0.0
    telemetry.semantic_viscosity = 2.0
    assert telemetry.semantic_viscosity == 1.0
    telemetry.semantic_viscosity = -1.0
    assert telemetry.semantic_viscosity == 0.0


def test_reflection_trail_timestamp_timezone(system: AxiomSystem) -> None:
    trail = system.meta_constraint.generate_auditable_reflection_trail(
        inference_context={"query": "ping", "semantic_entropy_level": 0.1},
        logical_dependencies=["fact_1"],
        existential_justifications=["adherence_to_axioms"],
    )
    timestamp = datetime.fromisoformat(trail["timestamp"])
    assert timestamp.tzinfo is not None
