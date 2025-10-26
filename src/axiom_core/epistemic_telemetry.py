# SPDX-License-Identifier: MPL-2.0
import time
from typing import Dict

class EpistemicTelemetry:
    """Tracks internal telemetry metrics."""

    def __init__(self):
        self._conscience_latency = 0.0
        self._gradient_decoherence = 0.0
        self._semantic_viscosity = 0.0
        self._coherence_flux = "AXIΩM v1.0 - Ethical Epistemology as a Service"

    @property
    def conscience_latency(self) -> float:
        return self._conscience_latency

    @conscience_latency.setter
    def conscience_latency(self, value: float):
        self._conscience_latency = value

    @property
    def gradient_decoherence(self) -> float:
        return self._gradient_decoherence

    @gradient_decoherence.setter
    def gradient_decoherence(self, value: float):
        self._gradient_decoherence = max(0.0, min(1.0, value))

    @property
    def semantic_viscosity(self) -> float:
        return self._semantic_viscosity

    @semantic_viscosity.setter
    def semantic_viscosity(self, value: float):
        self._semantic_viscosity = max(0.0, min(1.0, value))

    @property
    def coherence_flux(self) -> str:
        return self._coherence_flux

    def update_metrics(self, cli: float, gds: float, svm: float):
        self.conscience_latency = cli
        self.gradient_decoherence = gds
        self.semantic_viscosity = svm

    def get_all_metrics(self) -> Dict[str, float | str]:
        return {
            "Conscience Latency (CLI)": self.conscience_latency,
            "Gradient Decoherence (GDS)": self.gradient_decoherence,
            "Semantic Viscosity (SVM)": self.semantic_viscosity,
            "Coherence Flux": self.coherence_flux,
        }

    def simulate_introspection(self, duration_ms: float):
        start = time.perf_counter()
        time.sleep(duration_ms / 1000.0)
        end = time.perf_counter()
        self.conscience_latency = (end - start) * 1000.0
