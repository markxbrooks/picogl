"""
Generate Normal Data
"""

import numpy as np

from elmo.ui.state.scene.data import MolecularSceneState


def generate_normals(coords: np.ndarray) -> np.ndarray:
    """
    generate_normals

    :param coords: np.ndarray of shape (N, 3)
    :return: np.ndarray of shape (N, 3)
    Simple fake normals pointing up (for testing)
    """
    return np.tile(np.array([0.0, 0.0, 1.0], dtype=np.float32), (len(coords), 1))


def prepare_vertex_and_normal_data(mol_scene_state: MolecularSceneState) -> np.ndarray:
    """
    prepare_vertex_and_normal_data

    :param mol_scene_state: MolecularSceneState
    :return:

    prepare_vertex_and_normal_data
    """
    normals = generate_normals(mol_scene_state.coordinate_data_main.coords)
    return np.hstack([mol_scene_state.coordinate_data_main.coords, normals]).astype(
        np.float32
    )
