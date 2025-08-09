"""
upload_camera_matrices
"""

from elmo.ui.state.opengl import GLState
from elmo.ui.state.ui import UiState
from picogl.backend.modern.core.camera.matrix.compute import compute_camera_matrices
from picogl.shaders.matrix import upload_matrix


def upload_camera_matrices(
    ui_state: UiState, gl_state: GLState, width: int, height: int
) -> None:
    """
    Compute and upload the projection, view, and model matrices as shader_manager.current_shader_program uniforms.

    :param ui_state: UiState
    :param gl_state: GLState
    :param width: Viewport width in pixels.
    :type width: int
    :param height: Viewport height in pixels.
    :type height: int
    :return: None
    :rtype: None
    """
    projection, view, model = compute_camera_matrices(ui_state, width, height)
    gl_state.mvp_matrix = projection @ view @ model

    upload_matrix(
        gl_state.shader_manager.current_shader_program, "projection", projection
    )
    upload_matrix(gl_state.shader_manager.current_shader_program, "view", view)
    upload_matrix(gl_state.shader_manager.current_shader_program, "model", model)
