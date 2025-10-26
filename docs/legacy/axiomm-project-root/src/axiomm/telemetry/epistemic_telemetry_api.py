# SPDX-License-Identifier: MIT
# axiomm-project/src/axiomm/telemetry/epistemic_telemetry_api.py

import logging
import time
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EpistemicTelemetryAPI:
    """
    Manages and tracks the Epistemic Telemetry metrics as described in AXIΩM.
    This API is responsible for collecting, storing, and exposing the
    internal cognitive state metrics, including Incoherence Flux.
    """
    def __init__(self):
        self._conscience_latency = 0.0  # CLI: Reflects the time taken for introspection/ethical checks.
        self._gradient_decoherence = 0.0 # GDS: Represents the divergence from foundational principles during learning/evolution.
        self._semantic_viscosity = 0.0   # SVM: Measures the resistance to conceptual shifts or integration of new knowledge.
        self._coherence_flux = "AXIΩM v1.0 - Ethical Epistemology as a Service" # Conceptual version string
        self._epistemic_checksum = 0.0 # Derived from gradient norms, indicates current coherence
        self._incoherence_flux = 0.0   # Rate of change of epistemic checksum

    @property
    def conscience_latency(self) -> float:
        """Conscience Latency (CLI) in milliseconds."""
        return self._conscience_latency

    @property
    def gradient_decoherence(self) -> float:
        """Gradient Decoherence (GDS): Range 0.0 (perfect adherence) to 1.0 (maximal divergence)."""
        return self._gradient_decoherence

    @property
    def semantic_viscosity(self) -> float:
        """Semantic Viscosity (SVM): Range 0.0 (highly adaptive) to 1.0 (rigid)."""
        return self._semantic_viscosity

    @property
    def coherence_flux(self) -> str:
        """Coherence Flux: A high-level indicator of the system's overall state."""
        return self._coherence_flux

    @property
    def epistemic_checksum(self) -> float:
        """Epistemic Checksum: A numerical indicator of internal coherence/stability."""
        return self._epistemic_checksum

    @property
    def incoherence_flux(self) -> float:
        """Incoherence Flux: Rate of change of the epistemic checksum, indicating instability."""
        return self._incoherence_flux

    def update_epistemic_metrics(self,
                                 cli: Optional[float] = None,
                                 gds: Optional[float] = None,
                                 svm: Optional[float] = None,
                                 epistemic_checksum: Optional[float] = None,
                                 incoherence_flux: Optional[float] = None):
        """
        Updates selected epistemic telemetry metrics. Values are clamped for GDS/SVM.
        """
        if cli is not None:
            self._conscience_latency = cli
        if gds is not None:
            self._gradient_decoherence = max(0.0, min(1.0, gds))
        if svm is not None:
            self._semantic_viscosity = max(0.0, min(1.0, svm))
        if epistemic_checksum is not None:
            self._epistemic_checksum = epistemic_checksum
        if incoherence_flux is not None:
            self._incoherence_flux = incoherence_flux
        logging.debug("Epistemic telemetry metrics updated.")

    def get_all_metrics(self) -> Dict[str, Any]:
        """Returns all current telemetry metrics."""
        return {
            "Conscience Latency (CLI)": self.conscience_latency,
            "Gradient Decoherence (GDS)": self.gradient_decoherence,
            "Semantic Viscosity (SVM)": self.semantic_viscosity,
            "Epistemic Checksum": self.epistemic_checksum,
            "Incoherence Flux": self.incoherence_flux,
            "Coherence Flux Status": self.coherence_flux
        }

    def simulate_introspection_delay(self, duration_ms: float):
        """Simulates the cognitive load for introspection, updating CLI."""
        time.sleep(duration_ms / 1000.0)
        self.update_epistemic_metrics(cli=duration_ms)
        logging.debug(
            f"Simulated introspection delay of {duration_ms}ms, CLI: {self.conscience_latency:.2f}ms"
        )
