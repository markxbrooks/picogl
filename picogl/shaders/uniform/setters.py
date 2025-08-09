"""
OpenGL Shader Uniform Utilities
===============================

This module provides utility functions for setting various types of uniform variables
in OpenGL shader programs using both raw OpenGL and Qt's `QOpenGLShaderProgram` API.

It supports setting boolean, float, vector, and matrix uniforms, and includes error
handling and logging for common issues such as missing uniforms or incorrect matrix shapes.

Dependencies:
-------------
- numpy
- PySide6 (Qt GUI and OpenGL modules)
- OpenGL (PyOpenGL)
- picogl.logger (custom logging utility)

Functions:
----------

.. autofunction:: set_render_uniforms
    Sets a boolean uniform (`useHighlight`) using raw OpenGL calls.

.. autofunction:: set_qt_render_uniforms
    Binds a `QOpenGLShaderProgram` and validates its linkage status.

.. autofunction:: set_uniform_matrix
    Sets a 4x4 matrix uniform in a shader program.

.. autofunction:: set_uniform_float
    Sets a float uniform value.

.. autofunction:: set_uniform_vec3
    Sets a vec3 (3-component float vector) uniform.

.. autofunction:: set_uniform_bool
    Sets a boolean uniform value using integer representation.

Usage Example:
--------------

.. code-block:: python

    shader_program = QOpenGLShaderProgram()
    set_uniform_float(shader_program, b"u_opacity", 0.75)
    set_uniform_matrix(shader_program, b"u_mvp", np.identity(4, dtype=np.float32))

"""

import numpy as np
from OpenGL._bytes import bytes
from OpenGL.raw.GL._types import GL_FALSE
from OpenGL.raw.GL.VERSION.GL_2_0 import glUniform1f, glUniform1i, glUniform3f
from PySide6.QtGui import QOpenGLFunctions as gl
from PySide6.QtOpenGL import QOpenGLShaderProgram

from picogl.logger import Logger as log
from OpenGL.GL import *
from OpenGL.GL import glUniformMatrix4fv


def set_render_uniforms(shader_program: int) -> None:
    """
    set_render_uniforms

    :param shader_program: int Shader shader_program.
    :return: None

    Set uniform values using OpenGL's Shader Program API.
    """
    loc_highlight = gl.glGetUniformLocation(shader_program, b"useHighlight")
    if loc_highlight != -1:
        gl.glUniform1i(loc_highlight, gl.GL_FALSE)


def set_qt_render_uniforms(shader_program: QOpenGLShaderProgram) -> None:
    """
    set_qt_render_uniforms

    :param shader_program: QOpenGLShaderProgram instance
    :return: None

    Set uniform values using Qt's QOpenGLShaderProgram API.
    """
    if not isinstance(shader_program, QOpenGLShaderProgram):
        log.error(
            "❌ Provided shader_program is not a QOpenGLShaderProgram."
        )
        return

    if not shader_program.isLinked():
        log.error("❌ Shader shader_program is not linked.")
        return

    shader_program.bind()


def set_uniform_matrix(
    shader_program: QOpenGLShaderProgram, uniform_name: bytes, mvp_matrix: np.ndarray
) -> None:
    """
    set_uniform_matrix

    :param shader_program: QOpenGLShaderProgram
    :param uniform_name: Name of the uniform as a byte string (e.g., b"u_base_point_size").
    :param mvp_matrix: np.ndarray  The matrix to set.
    :return: None

    Sets a matrix uniform uniform_value in the shader_program.
    """
    if mvp_matrix.shape != (4, 4):
        log.error(f"❌ Uniform matrix must be 4x4, got shape {mvp_matrix.shape}")
        return

    uniform_location = shader_program.uniformLocation(uniform_name)
    if uniform_location == -1:
        log.error(
            f"❌ Uniform '{uniform_name.decode()}' not found in shader_program."
        )
        return
    try:
        # Transpose for column-major order, flatten, convert to list of 16 floats
        mvp_flat = mvp_matrix.astype(np.float32).T.flatten()
        glUniformMatrix4fv(uniform_location, 1, GL_FALSE, mvp_flat)
    except Exception as ex:
        log.error(f"❌ Error setting uniform matrix '{uniform_name.decode()}': {ex}")


def set_uniform_float(
    shader_program: QOpenGLShaderProgram, uniform_name: bytes, value: float
) -> None:
    """
    set_uniform_float

    :param shader_program: QOpenGLShaderProgram
    :param uniform_name: Name of the uniform as a byte string (e.g., b"u_base_point_size").
    :param value: The float uniform_value to set.
    :return: None

    Sets a float uniform uniform_value in the
    shader_manager.current_shader_program shader_program.
    """
    uniform_location = shader_program.uniformLocation(uniform_name)
    if uniform_location == -1:
        log.error(
            f"❌ Uniform '{uniform_name.decode()}' not found in shader_program."
        )
        return
    float_value = float(value)
    glUniform1f(uniform_location, float_value)


def set_uniform_vec3(
    shader_program: QOpenGLShaderProgram,
    uniform_name: bytes,
    vec3_value: tuple[float, float, float],
) -> None:
    """
    set_uniform_vec3

    :param shader_program: QOpenGLShaderProgram
    :param uniform_name: bytes
    :param vec3_value: tuple[float, float, float]
    :return: None
    """
    location = shader_program.uniformLocation(uniform_name)
    if location == -1:
        log.warning(
            f"⚠️ Uniform '{uniform_name.decode()}' not found in shader_program"
        )
        return
    glUniform3f(location, *vec3_value)


def set_uniform_bool(
    shader_program: QOpenGLShaderProgram, uniform_name: bytes, value: bool
) -> None:
    """
    set_uniform_bool

    :param shader_program: QOpenGLShaderProgram
    :param uniform_name: bytes
    :param value: bool
    :return: None
    """
    location = shader_program.uniformLocation(uniform_name)
    if location == -1:
        log.warning(
            f"⚠️ Uniform '{uniform_name.decode()}' not found in shader_program."
        )
        return
    glUniform1i(location, int(value))  # OpenGL expects bools as GLint
