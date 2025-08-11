from typing import Union

import numpy as np
from OpenGL.GL import *
from OpenGL.GL import glGetUniformLocation, glUniformMatrix4fv
from pyglm import glm

from picogl.backend.modern.core.shader.shader import PicoGLShader
from picogl.logger import Logger as log


def set_uniform_value(
    shader_program: int,
    uniform_name: str,
    uniform_value: Union[
        float, int, glm.vec2, glm.vec3, glm.vec4, glm.mat4, np.ndarray
    ],
):
    """
    set_uniform_value

    :param shader_program: int
    :param uniform_name: Name of the uniform variable
    :param uniform_value: Value to set (supports float, int, vec2, vec3, vec4, mat4, or np.ndarray)

    Set a uniform variable in a shader program
    """
    location = glGetUniformLocation(shader_program, uniform_name)
    if location == -1:
        log.warning(f"Uniform '{uniform_name}' not found in shader.")
        return
    set_uniform_location_value(location, uniform_value)

def set_uniform_location_value(location: int, uniform_value: Union[
        float, int, glm.vec2, glm.vec3, glm.vec4, glm.mat4, np.ndarray
    ]):
    """
    set_uniform_value

    :param uniform location:  int
    :param uniform_value: Value to set (supports float, int, vec2, vec3, vec4, mat4, or np.ndarray)

    Set a uniform variable in a shader program
    """
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
                f"Unsupported ndarray shape {uniform_value.shape} for uniform '{location}'"
            )
    else:
        log.warning(
            f"Unsupported uniform type for '{location}': {type(uniform_value)}"
        )


def shader_uniform_set_mvp(shader_program: int,
                           mvp_matrix: np.ndarray | glm.mat4
):
    """
    shader_uniform_set_mvp

    :param mvp_matrix: np.ndarray or glm.mat4 - model-view-projection matrix
    :param shader_program: int
    :return: None
    """
    mvp_loc = glGetUniformLocation(shader_program, "mvp")
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


def set_mvp_uniform(shader: PicoGLShader = None, mvp: glm.mat4 = None) -> None:
    """
    set_mvp_uniform

    :param shader:
    :param mvp:
    :return: None
    Set the model-view-projection matrix uniform in the shader program.
    """
    mvp_loc = glGetUniformLocation(shader.program, "mvp_matrix")
    glUniformMatrix4fv(mvp_loc, 1, GL_FALSE, glm.value_ptr(mvp))
