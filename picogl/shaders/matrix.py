import numpy as np

from OpenGL.GL import glGetUniformLocation, glUniformMatrix4fv
from OpenGL.GL.shaders import GL_TRUE


def upload_matrix(shader_program: int, name: str, matrix: np.ndarray) -> None:
    """
    upload_matrix

    :param shader_program: int
    :param name: str
    :param matrix: np.ndarray
    :return:
    """
    loc = glGetUniformLocation(shader_program, name)
    if loc != -1:
        glUniformMatrix4fv(loc, 1, GL_TRUE, matrix.astype(np.float32))
