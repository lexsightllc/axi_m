import time
import json
import random
from typing import Dict, Any, List

class MockOpenTelemetry:
    def __init__(self):
        self.metrics = {}
    
    def record_metric(self, name: str, value: Any, labels: Dict[str, str] = None):
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append({"value": value, "labels": labels, "timestamp": time.time()})

    def get_metrics(self) -> Dict[str, List[Dict[str, Any]]]:
        return self.metrics

class MockHardwareMonitor:
    def __init__(self):
        self._current_ipc_stalls = 0
        self._current_cache_misses = 0.0
        self._current_jitter = 0.0

    def simulate_hardware_metrics(self, load_intensity: float = 1.0):
        self._current_ipc_stalls = int(random.gauss(50 * load_intensity, 10 * load_intensity))
        self._current_cache_misses = random.gauss(0.01 * load_intensity, 0.005 * load_intensity)
        self._current_jitter = random.gauss(0.05 * load_intensity, 0.02 * load_intensity)
        self._current_ipc_stalls = max(0, self._current_ipc_stalls)
        self._current_cache_misses = max(0.0, min(1.0, self._current_cache_misses))
        self._current_jitter = max(0.0, self._current_jitter)

    def get_hardware_data(self) -> Dict[str, Any]:
        return {
            "ipc_stalls_per_sec": self._current_ipc_stalls,
            "cache_miss_rate": self._current_cache_misses,
            "attention_pipeline_jitter": self._current_jitter,
            "timestamp": time.time()
        }

class EpistemicTelemetryAPI:
    def __init__(self):
        self.otel = MockOpenTelemetry()
        self.hw_monitor = MockHardwareMonitor()
        self.coherence_flux_history: List[float] = []
        self._last_checksum: float = 0.0
        print("[TelemetryAPI] Epistemic Telemetry API initialized.")

    def update_epistemic_metrics(self,
                                 epistemic_checksum: float,
                                 gradient_decoherence_spectra: List[float],
                                 semantic_viscosity_value: float,
                                 conscience_latency_index: float,
                                 incoherence_flux_value: float,
                                 load_intensity: float = 1.0):
        self.otel.record_metric("epistemic.checksum", epistemic_checksum)
        self.otel.record_metric("epistemic.gradient_decoherence_spectra", gradient_decoherence_spectra)
        self.otel.record_metric("epistemic.semantic_viscosity_map", semantic_viscosity_value)
        self.otel.record_metric("epistemic.conscience_latency_index", conscience_latency_index)
        self.otel.record_metric("epistemic.incoherence_flux", incoherence_flux_value)

        self.coherence_flux_history.append(incoherence_flux_value)
        self._last_checksum = epistemic_checksum

        self.hw_monitor.simulate_hardware_metrics(load_intensity)
        hw_data = self.hw_monitor.get_hardware_data()
        for k, v in hw_data.items():
            self.otel.record_metric(f"hardware.{k}", v)

    def get_realtime_telemetry(self) -> Dict[str, Any]:
        current_metrics = self.otel.get_metrics()
        latest_cli = current_metrics.get("epistemic.conscience_latency_index", [{}])[-1].get("value", 0.0)
        latest_gds = current_metrics.get("epistemic.gradient_decoherence_spectra", [{}])[-1].get("value", [])
        latest_svm = current_metrics.get("epistemic.semantic_viscosity_map", [{}])[-1].get("value", 0.0)
        latest_flux = current_metrics.get("epistemic.incoherence_flux", [{}])[-1].get("value", 0.0)
        latest_checksum = current_metrics.get("epistemic.checksum", [{}])[-1].get("value", 0.0)
        return {
            "ConscienceLatencyIndex_CLI": latest_cli,
            "GradientDecoherenceSpectra_GDS": latest_gds,
            "SemanticViscosityMap_SVM": latest_svm,
            "CoherenceFlux": latest_flux,
            "EpistemicChecksum": latest_checksum,
            "CoherenceFluxHistory": self.coherence_flux_history[-10:],
            "HardwareLoadMetrics": self.hw_monitor.get_hardware_data()
        }

    def get_full_metric_log(self) -> Dict[str, List[Dict[str, Any]]]:
        return self.otel.get_metrics()

if __name__ == "__main__":
    telemetry_api = EpistemicTelemetryAPI()

    print("--- Simulating Telemetry Updates (Normal Operation) ---")
    for i in range(5):
        checksum_val = 100 + i * 0.1
        flux_val = 0.01 * i
        telemetry_api.update_epistemic_metrics(
            epistemic_checksum=checksum_val,
            gradient_decoherence_spectra=[0.1 + i*0.01, 0.05 - i*0.005],
            semantic_viscosity_value=1.0 + i*0.05,
            conscience_latency_index=5 + i,
            incoherence_flux_value=flux_val,
            load_intensity=1.0
        )
        time.sleep(0.1)
        print(f"Update {i+1}: Current CLI={telemetry_api.get_realtime_telemetry()['ConscienceLatencyIndex_CLI']:.2f}")

    print("\n--- Simulating Telemetry Updates (High Epistemic Tension / Singularity) ---")
    for i in range(5):
        checksum_val = 105 + i * 2.0
        flux_val = 1.0 + i * 0.5
        telemetry_api.update_epistemic_metrics(
            epistemic_checksum=checksum_val,
            gradient_decoherence_spectra=[0.8 + i*0.02, 0.7 - i*0.01],
            semantic_viscosity_value=5.0 + i*0.8,
            conscience_latency_index=50 + i*10,
            incoherence_flux_value=flux_val,
            load_intensity=2.5
        )
        time.sleep(0.1)
        print(f"Update {i+1}: Current CLI={telemetry_api.get_realtime_telemetry()['ConscienceLatencyIndex_CLI']:.2f}, "
              f"Current Flux={telemetry_api.get_realtime_telemetry()['CoherenceFlux']:.2f}, "
              f"IPC Stalls={telemetry_api.get_realtime_telemetry()['HardwareLoadMetrics']['ipc_stalls_per_sec']}")

    print("\n--- Final Telemetry Snapshot ---")
    snapshot = telemetry_api.get_realtime_telemetry()
    print(json.dumps(snapshot, indent=2))
