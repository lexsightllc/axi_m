# axiomm-project/src/axiomm/core/axiomatic_singularity.py

import numpy as np
import logging
from typing import Dict, Any, Tuple, List, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AxiomaticSingularityDetector:
    """
    Detects axiomatic singularities by analyzing divergence in latent representations
    and gradient fields relative to foundational axioms. This component formalizes
    the 'Trigger Condition' of the self-stabilizing uncertainty manifold.
    """
    def __init__(self, epsilon_axiom: float = 0.1):
        """
        Initializes the detector with a sensitivity threshold.

        Args:
            epsilon_axiom (float): Sensitivity threshold for gradient divergence.
                                   Smaller values detect singularities more easily.
        """
        self.epsilon_axiom = epsilon_axiom
        logging.info(f"AxiomaticSingularityDetector initialized with epsilon_axiom: {self.epsilon_axiom}")

    def detect(
               self,
               latent_representation: np.ndarray,
               gradient_field: Dict[str, np.ndarray],
               attractor_basins: Dict[str, np.ndarray],
               axioms: List[str]) -> Tuple[bool, Optional[str]]:
        """
        Detects an axiomatic singularity (or 'null-consistent bifurcation node')
        based on:
        1. Divergent Gradient Consensus: High difference in gradients projecting
           onto different axiomatic spaces.
        2. Non-Isomorphic Projections / Topological Properties: The latent
           representation points to logically opposite directions (divergent signs)
           relative to conflicting attractor basins.

        Args:
            latent_representation (np.ndarray): The current latent representation of the query (L).
            gradient_field (Dict[str, np.ndarray]): Gradients of projection onto different axiomatic spaces (∇L).
                                                    Keys are axiom names, values are gradient vectors.
            attractor_basins (Dict[str, np.ndarray]): Vector representations of axiomatic attractor basins (B_i).
            axioms (List[str]): List of active axiomatic constraints (A_i).

        Returns:
            Tuple[bool, Optional[str]]: True if a singularity is detected, along with
                                        the conceptual "bifurcation node" (e.g., the conflicting axiom).
        """
        logging.info("Detecting axiomatic singularities.")

        # store for inspection/testing
        self.gradient_field = gradient_field
        self.attractor_basins = attractor_basins

        # Ensure we have at least two axioms to compare for divergence
        if len(axioms) < 2:
            logging.debug("Fewer than 2 axioms provided, no singularity detection possible conceptually.")
            return False, None

        max_grad_diff = 0.0
        divergent_signs = False
        bifurcation_node = None

        # Conceptual check for Divergent Gradient Consensus and Non-Isomorphic Projections
        # A real system would use more sophisticated metrics like cosine similarity of gradients
        # or topological data analysis of latent space clusters relative to axiom embeddings.
        for i in range(len(axioms)):
            for j in range(i + 1, len(axioms)):
                axiom1 = axioms[i]
                axiom2 = axioms[j]

                grad1 = gradient_field.get(axiom1)
                grad2 = gradient_field.get(axiom2)
                basin1 = attractor_basins.get(axiom1)
                basin2 = attractor_basins.get(axiom2)

                if grad1 is None or grad2 is None or basin1 is None or basin2 is None:
                    continue  # Skip if data for axioms is missing

                # 1. Divergence of Gradient (conceptual: Euclidean distance between gradient vectors)
                # Represents |∇L(A_i) - ∇L(A_j)|
                grad_diff = np.linalg.norm(grad1 - grad2)
                if grad_diff > max_grad_diff:
                    max_grad_diff = grad_diff

                # 2. Non-Isomorphic Projections (conceptual: sign difference of dot products)
                # Represents sign(L · B_i) != sign(L · B_j)
                # Meaning the latent representation is pulled in opposite conceptual directions
                # by different axiomatic basins.
                if np.sign(np.dot(latent_representation, basin1)) != np.sign(np.dot(latent_representation, basin2)):
                    divergent_signs = True
                    bifurcation_node = f"Conflict between '{axiom1}' and '{axiom2}'"
                    break  # Found divergent signs, sufficient for this conceptual model
            if divergent_signs:
                break

        # A singularity is detected if both conditions are met, signifying an axiomatic collision.
        is_singularity = (max_grad_diff > self.epsilon_axiom and divergent_signs)

        if is_singularity:
            logging.warning(f"Axiomatic singularity detected (Bifurcation Node: {bifurcation_node}).")
            logging.debug(f"Max Gradient Diff: {max_grad_diff:.4f}, Divergent Signs: {divergent_signs}")
        else:
            logging.debug(f"No axiomatic singularity detected. Max Gradient Diff: {max_grad_diff:.4f}, Divergent Signs: {divergent_signs}")

        return is_singularity, bifurcation_node
