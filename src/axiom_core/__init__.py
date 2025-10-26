"""Public interface for the AXIΩM ontological core."""

from .axiom_system import AxiomSystem
from .epistemic_telemetry import EpistemicTelemetry
from .ethical_manifolds import (
    HobbesianSocialContractarianManifold,
    KantianDeontologicalManifold,
    UtilitarianConsequentialistManifold,
)
from .meta_constraint import MetaConstraint

__all__ = [
    "AxiomSystem",
    "EpistemicTelemetry",
    "HobbesianSocialContractarianManifold",
    "KantianDeontologicalManifold",
    "MetaConstraint",
    "UtilitarianConsequentialistManifold",
]
