from typing import Union

import numpy as np
from pyglm import glm
from PySide6.QtOpenGL import QOpenGLShaderProgram

from elmo.logger import Logger as log
from elmo.utils.shaderLoader import Shader
from OpenGL.GL import *
from OpenGL.GL import glGetUniformLocation, glUniformMatrix4fv


def set_uniform_value(
    qt_shader_program: QOpenGLShaderProgram,
    uniform_name: str,
    uniform_value: Union[
        float, int, glm.vec2, glm.vec3, glm.vec4, glm.mat4, np.ndarray
    ],
):
    """
    set_uniform_value

    :param qt_shader_program: QOpenGLShaderProgram
    :param uniform_name: Name of the uniform variable
    :param uniform_value: Value to set (supports float, int, vec2, vec3, vec4, mat4, or np.ndarray)

    Set a uniform variable in a shader program
    """
    location = glGetUniformLocation(qt_shader_program.programId(), uniform_name)
    if location == -1:
        log.warning(f"Uniform '{uniform_name}' not found in shader.")
        return

    # Handle types
    if isinstance(uniform_value, float):
        glUniform1f(location, uniform_value)
    elif isinstance(uniform_value, int):
        glUniform1i(location, uniform_value)
    elif isinstance(uniform_value, glm.vec2):
        glUniform2fv(location, 1, glm.value_ptr(uniform_value))
    elif isinstance(uniform_value, glm.vec3):
        glUniform3fv(location, 1, glm.value_ptr(uniform_value))
    elif isinstance(uniform_value, glm.vec4):
        glUniform4fv(location, 1, glm.value_ptr(uniform_value))
    elif isinstance(uniform_value, glm.mat4):
        glUniformMatrix4fv(location, 1, GL_FALSE, glm.value_ptr(uniform_value))
    elif isinstance(uniform_value, np.ndarray):
        if uniform_value.shape == (4, 4):  # mat4
            glUniformMatrix4fv(
                location, 1, GL_FALSE, uniform_value.astype(np.float32).flatten()
            )
        elif uniform_value.shape == (3,):  # vec3
            glUniform3fv(location, 1, uniform_value.astype(np.float32))
        elif uniform_value.shape == (4,):  # vec4
            glUniform4fv(location, 1, uniform_value.astype(np.float32))
        else:
            log.warning(
                f"Unsupported ndarray shape {uniform_value.shape} for uniform '{uniform_name}'"
            )
    else:
        log.warning(
            f"Unsupported uniform type for '{uniform_name}': {type(uniform_value)}"
        )


def shader_uniform_set_mvp(
    qt_shader_program: QOpenGLShaderProgram, mvp_matrix: np.ndarray | glm.mat4
):
    """
    shader_uniform_set_mvp

    :param mvp_matrix: np.ndarray or glm.mat4 - Model-View-Projection matrix
    :param qt_shader_program: QOpenGLShaderProgram
    :return: None
    """
    mvp_loc = glGetUniformLocation(qt_shader_program.programId(), "mvp")
    if mvp_loc == -1:
        log.warning("Uniform 'mvp' not found in shader.")
    else:
        # Convert numpy data or glm.mat4 to float pointer
        if isinstance(mvp_matrix, np.ndarray):
            glUniformMatrix4fv(
                mvp_loc, 1, GL_FALSE, mvp_matrix.astype(np.float32).flatten()
            )
        else:
            glUniformMatrix4fv(mvp_loc, 1, GL_FALSE, glm.value_ptr(mvp_matrix))


def set_mvp_uniform(shader: Shader = None, mvp: glm.mat4 = None) -> None:
    """
    set_mvp_uniform

    :param shader:
    :param mvp:
    :return: None
    Set the model-view-projection matrix uniform in the shader program.
    """
    mvp_loc = glGetUniformLocation(shader.program, "mvp_matrix")
    glUniformMatrix4fv(mvp_loc, 1, GL_FALSE, glm.value_ptr(mvp))
