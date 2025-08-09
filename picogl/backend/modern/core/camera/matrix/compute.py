"""
Compute camera matrices for OpenGL rendering.

This module defines the `compute_camera_matrices` function, which generates the
projection, view, and model transformation matrices required to render a 3D scene
based on the current camera state stored in a `UiState` object.

The output matrices are NumPy arrays and are used to configure the shader_manager.current_shader_program's mvp_matrix
(model-view-projection) pipeline.

Functions:
----------
- compute_camera_matrices(ui_state: UiState, width: int, height: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]
    Computes and returns the projection, view, and model matrices based on the
    current UI and camera state, viewport width and height.

Dependencies:
-------------
- numpy
- elmo.picogl.backend.camera.numpy.update_camera_matrix
- elmo.picogl.backend.matrix.numpy.perspective
- elmo.picogl.backend.matrix.numpy.look_at
- elmo.ui.state.ui.UiState

Usage example:
--------------
>>> from elmo.ui.state.ui import UiState
>>> ui_state = UiState()
>>> width, height = 800, 600
>>> projection, view, model = compute_camera_matrices(ui_state, width, height)

"""

import numpy as np

from elmo.ui.state.ui import UiState
from picogl.backend.modern.core.camera.matrix.update import update_camera_matrix
from picogl.backend.legacy.core.camera.look_at import look_at, perspective


def compute_camera_matrices(
    ui_state: UiState, width: int, height: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    compute_camera_matrices

    :param ui_state: UiState object
    :param width: Viewport width.
    :param height: Viewport height.
    :return: Tuple of (projection, view, model) matrices.
    :rtype: tuple[np.ndarray, np.ndarray, np.ndarray]
    Compute projection, view, and model matrices for the current camera state.
    """
    height = max(height, 1)
    projection = perspective(45.0, width / height, 0.1, 1000.0)
    view = look_at(
        eye=np.array(ui_state.camera.position, dtype=np.float32),
        target=np.array(ui_state.camera.target, dtype=np.float32),
        up=np.array([0, 1, 0], dtype=np.float32),
    )
    model = update_camera_matrix(
        ui_state.camera.translation,
        ui_state.camera.rotation,
        ui_state.camera.zoom.value,
    )
    return projection, view, model
