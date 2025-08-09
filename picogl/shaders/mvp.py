import numpy as np
from PySide6.QtGui import QMatrix4x4
from PySide6.QtGui import QOpenGLFunctions as gl
from PySide6.QtOpenGL import QOpenGLShaderProgram

from picogl.logger import Logger as log
from OpenGL.GL import glUniformMatrix4fv
from OpenGL.GL.shaders import GL_FALSE
from picogl.error import check_errors


def use_non_qt_shader_with_mvp(shader_program: int, mvp_matrix: np.ndarray):
    """
    use_shader_with_mvp

    :param shader_program: int
    :param mvp_matrix:
    :return:
    """
    check_errors()
    # glUseProgram(shader_manager.current_shader_program)
    mvp_loc = gl.glGetUniformLocation(shader_program, "mvp_matrix")
    if mvp_loc != -1:
        gl.glUniformMatrix4fv(mvp_loc, 1, gl.GL_TRUE, mvp_matrix.astype(np.float32))
    else:
        print(
            "⚠️ Warning: 'mvp_matrix' uniform not found in shader_manager.current_shader_program"
        )
    check_errors()


def ortho_matrix_flat(left, right, bottom, top, near, far):
    mat = np.array(
        [
            [2 / (right - left), 0, 0, -(right + left) / (right - left)],
            [0, 2 / (top - bottom), 0, -(top + bottom) / (top - bottom)],
            [0, 0, -2 / (far - near), -(far + near) / (far - near)],
            [0, 0, 0, 1],
        ],
        dtype=np.float32,
    )
    return mat.T.flatten().tolist()


mvp_ortho_flat = ortho_matrix_flat(-1, 1, -1, 1, -1, 1)


def use_shader_with_mvp(
    shader_program: QOpenGLShaderProgram, mvp_matrix: np.ndarray
) -> None:
    """
    Uploads mvp_matrix matrix to shader_manager.current_shader_program using Qt's shader_manager.current_shader_program API.

    :param shader_program: QOpenGLShaderProgram
    :param mvp_matrix: np.ndarray of shape (4, 4)
    """
    check_errors()
    shader_program.bind()

    if not shader_program.isLinked():
        log.error("❌ Shader shader_program is not linked.")
        return

    if mvp_matrix.shape != (4, 4):
        log.error("❌ mvp_matrix matrix must be 4x4")
        return

    try:
        # Transpose for column-major order, flatten, convert to list of 16 floats
        mvp_flat = mvp_matrix.astype(np.float32).T.flatten()

        # Debug uniform location
        loc = shader_program.uniformLocation(b"mvp_matrix")
        if loc == -1:
            log.error(
                "❌ 'mvp_matrix' uniform not found in shader_manager.current_shader_program"
            )
            return

        glUniformMatrix4fv(loc, 1, GL_FALSE, mvp_flat)
    except Exception as ex:
        log.error(f"❌ Error setting mvp_matrix uniform: {ex}")
