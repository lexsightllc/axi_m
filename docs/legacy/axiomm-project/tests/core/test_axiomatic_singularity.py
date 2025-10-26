import pytest
import numpy as np
from src.axiomm.core.axiomatic_singularity import AxiomaticSingularityDetector

@pytest.fixture
def detector():
    return AxiomaticSingularityDetector(epsilon_axiom=0.5)

def test_no_singularity_coherent_gradients(detector):
    x_coherent = np.array([0.1, 0.1, 0.1])
    grad_a = np.array([0.2, 0.2, 0.2])
    grad_b = np.array([0.3, 0.3, 0.3])
    basin_a = np.array([1.0, 0.0, 0.0])
    basin_b = np.array([1.0, 0.0, 0.0])
    gradient_field = {'axiom_a': grad_a, 'axiom_b': grad_b}
    attractor_basins = {'axiom_a': basin_a, 'axiom_b': basin_b}
    axioms = ['axiom_a', 'axiom_b']
    is_singularity, _ = detector.detect(x_coherent, gradient_field, attractor_basins, axioms)
    assert not is_singularity

def test_singularity_divergent_gradients_and_signs(detector):
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
    is_singularity, bifurcation_node = detector.detect(x_dilemma, gradient_field, attractor_basins, axioms)
    assert is_singularity
    assert "bifurcation_node" in bifurcation_node

def test_singularity_high_gradient_diff_but_no_sign_divergence(detector):
    x_dilemma = np.array([0.5, 0.2, 0.8])
    grad_a = np.array([1.0, 0.1, 0.9])
    grad_b = np.array([0.0, 0.1, 0.0])
    basin_a = np.array([1.0, 0.0, 0.0])
    basin_b = np.array([0.9, 0.0, 0.0])
    gradient_field = {'axiom_a': grad_a, 'axiom_b': grad_b}
    attractor_basins = {'axiom_a': basin_a, 'axiom_b': basin_b}
    axioms = ['axiom_a', 'axiom_b']
    is_singularity, _ = detector.detect(x_dilemma, gradient_field, attractor_basins, axioms)
    assert not is_singularity

def test_insufficient_axioms(detector):
    x = np.array([0.1])
    grad_a = np.array([0.2])
    basin_a = np.array([1.0])
    gradient_field = {'axiom_a': grad_a}
    attractor_basins = {'axiom_a': basin_a}
    axioms = ['axiom_a']
    is_singularity, reason = detector.detect(x, gradient_field, attractor_basins, axioms)
    assert not is_singularity
    assert "No sufficient axioms" in reason

def test_missing_gradient_or_basin_data(detector):
    x = np.array([0.1, 0.1])
    grad_a = np.array([0.2, 0.2])
    basin_a = np.array([1.0, 0.0])
    gradient_field = {'axiom_a': grad_a}
    attractor_basins = {'axiom_a': basin_a, 'axiom_b': np.array([-1.0, 0.0])}
    axioms = ['axiom_a', 'axiom_b']
    is_singularity, reason = detector.detect(x, gradient_field, attractor_basins, axioms)
    assert not is_singularity
    assert "Insufficient gradient or basin data" in reason
