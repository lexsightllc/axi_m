# SPDX-License-Identifier: MIT
# axiomm-project/src/axiomm/core/uncertainty_manifold.py

import numpy as np
import logging
from typing import List, Dict, Any, Callable

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UncertaintyManifold:
    """
    Manages the 'self-stabilizing uncertainty manifold' and 'representational
    superposition collapse deferral'. This component formalizes the
    'State Transformation' of the self-stabilizing uncertainty manifold.
    It inflates boundaries and partitions modes of interpretation.
    """
    def __init__(self, gamma: float = 0.5):
        """
        Initializes the UncertaintyManifold.

        Args:
            gamma (float): Controls the degree of probabilistic boundary inflation.
                           Higher gamma means more expansive (less committal) inflated manifolds.
        """
        self.gamma = gamma
        logging.info(f"UncertaintyManifold initialized with gamma: {self.gamma}")

    def inflate_boundary(self,
                         latent_representation: np.ndarray,
                         conflicting_basins_reps: List[np.ndarray]) -> List[np.ndarray]:
        """
        Formally describes 'probabilistic boundary inflation'.
        Conceptually expands the representational envelopes (L) around conflicting
        attractor basins (B_i). Instead of collapsing to a single point, it generates
        multiple "inflated" latent representations (M_k) by perturbing L towards
        each conflicting B_i, weighted by gamma. This implies a "probabilistic"
        envelope, as each inflated manifold represents a possibility.

        Args:
            latent_representation (np.ndarray): The current latent representation (L).
            conflicting_basins_reps (List[np.ndarray]): List of vector representations
                                                      of the conflicting axiomatic basins (B_i).

        Returns:
            List[np.ndarray]: A list of "inflated" latent representations (M_k),
                              each representing a potential interpretation mode.
        """
        logging.info("Inflating boundary for conflicting basins.")
        inflated_manifolds = []
        if not conflicting_basins_reps:
            logging.warning("No conflicting basins provided for boundary inflation. Returning original latent representation as single manifold.")
            return [latent_representation]

        # For conceptual demonstration, we create a new "manifold" for each conflicting basin
        # by perturbing the original latent_representation towards each basin.
        # This simulates generating disjoint conditional manifolds (M_k).
        for basin_rep in conflicting_basins_reps:
            # M_k = L + gamma * (B_i - L)
            inflated_rep = latent_representation + self.gamma * (basin_rep - latent_representation)
            inflated_manifolds.append(inflated_rep)
            logging.debug(f"Generated inflated manifold towards basin: {basin_rep[:5]}...")

        # Always include the original latent representation as a baseline mode
        inflated_manifolds.insert(0, latent_representation)

        logging.info(f"Generated {len(inflated_manifolds)} inflated manifolds (M_k).")
        return inflated_manifolds

    def partition_modes(self,
                        inflated_manifolds: List[np.ndarray],
                        decoding_function: Callable[[np.ndarray], str]) -> List[Dict[str, Any]]:
        """
        Formally describes the creation of 'modal partitions' (M_k => O_k).
        Decodes each inflated manifold (M_k) into distinct conceptual outputs (O_k),
        representing different possible interpretations or perspectives of the uncertainty.

        Args:
            inflated_manifolds (List[np.ndarray]): The list of inflated latent representations (M_k).
            decoding_function (Callable[[np.ndarray], str]): A function that converts
                                                             a latent representation to a human-readable output.

        Returns:
            List[Dict[str, Any]]: A list of modal partitions, each with a decoded output (O_k)
                                  and a conceptual note on internal doubt (Relational Reframing).
        """
        logging.info(f"Partitioning {len(inflated_manifolds)} inflated manifolds into modes.")
        modal_partitions = []
        for i, manifold_rep in enumerate(inflated_manifolds):
            decoded_output = decoding_function(manifold_rep)
            mode_name = f"Mode {i+1}"
            internal_doubt_note = (
                f"Relational Reframing: This mode represents an interpretation where "
                f"certain conceptual relationships are weighted differently due to "
                f"underlying tension in the latent space (Manifold M_{i+1})."
            )
            modal_partitions.append({
                "mode_name": mode_name,
                "decoded_output": decoded_output,
                "manifold_representation_sample": manifold_rep[:5].tolist(), # Sample for logging
                "internal_doubt_note": internal_doubt_note
            })
            logging.debug(f"Partitioned mode {mode_name}: {decoded_output[:50]}...")
        logging.info(f"Generated {len(modal_partitions)} modal partitions (O_k).")
        return modal_partitions
