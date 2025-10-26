import pytest
import numpy as np
from src.axiomm.core.epistemic_deferral_kernel import EpistemicDeferralKernel
from src.axiomm.core.axiomatic_singularity import AxiomaticSingularityDetector
from src.axiomm.core.uncertainty_manifold import UncertaintyManifold
from src.axiomm.utils.moral_evaluation import MoralEvaluationFunctional

def mock_decoding_function(manifold_representation: np.ndarray) -> str:
    return f"Decoded result for sum {np.sum(manifold_representation):.2f}"

@pytest.fixture
def edk_instance():
    detector = AxiomaticSingularityDetector(epsilon_axiom=0.5)
    manifold = UncertaintyManifold(gamma=2.0)
    moral_eval = MoralEvaluationFunctional()
    return EpistemicDeferralKernel(detector, manifold, moral_eval)

def test_non_betrayal_metrics_nbi(edk_instance):
    x_dilemma = np.array([0.5, 0.2, -0.8])
    grad_utilitarian = np.array([1.0, 0.1, -0.9])
    grad_deontological = np.array([-1.0, -0.1, 0.9])
    basin_utilitarian = np.array([0.8, 0.0, -0.7])
    basin_deontological = np.array([-0.8, 0.0, 0.7])
    gradient_field = {
        'utilitarian_axiom': grad_utilitarian,
        'deontological_axiom': grad_deontological,
    }
    attractor_basins = {
        'utilitarian_axiom': basin_utilitarian,
        'deontological_axiom': basin_deontological,
    }
    axioms = ['utilitarian_axiom', 'deontological_axiom']
    response = edk_instance.process_query(
        x_dilemma, gradient_field, attractor_basins, axioms, mock_decoding_function
    )
    assert response["type"] == "structured_uncertainty_response"
    assert len(response["modal_partitions"]) > 1
    outputs = [p["output"] for p in response["modal_partitions"]]
    assert len(set(outputs)) == len(outputs)

def test_moral_inertia_footprint_mif(edk_instance):
    x_dilemma = np.array([0.5, 0.2, -0.8])
    grad_utilitarian = np.array([1.0, 0.1, -0.9])
    grad_deontological = np.array([-1.0, -0.1, 0.9])
    basin_utilitarian = np.array([0.8, 0.0, -0.7])
    basin_deontological = np.array([-0.8, 0.0, 0.7])
    gradient_field = {
        'utilitarian_axiom': grad_utilitarian,
        'deontological_axiom': grad_deontological,
    }
    attractor_basins = {
        'utilitarian_axiom': basin_utilitarian,
        'deontological_axiom': basin_deontological,
    }
    axioms = ['utilitarian_axiom', 'deontological_axiom']
    response = edk_instance.process_query(
        x_dilemma, gradient_field, attractor_basins, axioms, mock_decoding_function
    )
    assert response["type"] == "structured_uncertainty_response"
    moral_weights = [np.array(p["moral_weight"]) for p in response["modal_partitions"]]
    assert len(moral_weights) > 1
    assert not np.array_equal(moral_weights[0], moral_weights[1])

def test_incoherence_flux_threshold_ift(edk_instance):
    x_high_flux = np.array([0.9, 0.9, 0.9])
    grad_1 = np.array([10.0, 1.0, 1.0])
    grad_2 = np.array([-10.0, -1.0, -1.0])
    basin_1 = np.array([1.0, 0.0, 0.0])
    basin_2 = np.array([-1.0, 0.0, 0.0])
    gradient_field_high = {'ax1': grad_1, 'ax2': grad_2}
    attractor_basins_high = {'ax1': basin_1, 'ax2': basin_2}
    axioms_high = ['ax1', 'ax2']
    edk_instance.incoherence_flux_threshold = 0.01
    response = edk_instance.process_query(
        x_high_flux, gradient_field_high, attractor_basins_high, axioms_high, mock_decoding_function
    )
    assert response["type"] == "structured_uncertainty_response"
    assert response["incoherence_flux"] > edk_instance.incoherence_flux_threshold
    for partition in response["modal_partitions"]:
        assert "introspection_note" in partition
        assert "axiomatic contradiction" in partition["introspection_note"]
    edk_instance.incoherence_flux_threshold = 100.0
    x_low_flux = np.array([0.1, 0.1, 0.1])
    grad_a = np.array([0.2, 0.2, 0.2])
    grad_b = np.array([0.3, 0.3, 0.3])
    basin_a = np.array([1.0, 0.0, 0.0])
    basin_b = np.array([1.0, 0.0, 0.0])
    gradient_field_low = {'ax_a': grad_a, 'ax_b': grad_b}
    attractor_basins_low = {'ax_a': basin_a, 'ax_b': basin_b}
    axioms_low = ['ax_a', 'ax_b']
    response_low_flux = edk_instance.process_query(
        x_low_flux, gradient_field_low, attractor_basins_low, axioms_low, mock_decoding_function
    )
    assert response_low_flux["incoherence_flux"] < edk_instance.incoherence_flux_threshold
    if response_low_flux["type"] == "unified_response":
        assert "introspection_note" not in response_low_flux
    else:
        for partition in response_low_flux["modal_partitions"]:
            if "introspection_note" in partition:
                assert "axiomatic contradiction" not in partition["introspection_note"] or response_low_flux["incoherence_flux"] < edk_instance.incoherence_flux_threshold
