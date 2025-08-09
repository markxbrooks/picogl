"""
Common Shader Uniforms
"""

from typing import Tuple

import numpy as np
from OpenGL._bytes import bytes
from PySide6.QtOpenGL import QOpenGLShaderProgram

from picogl.logger import Logger as log
from picogl.shaders.uniform.setters import (set_uniform_bool,
                                            set_uniform_float,
                                            set_uniform_matrix,
                                            set_uniform_vec3)


def set_common_shader_uniforms(
    shader: QOpenGLShaderProgram,
    point_size: float = 10.0,
    highlight: bool = False,
    highlight_color: tuple = (1.0, 1.0, 1.0),
    line_color: tuple = (1.0, 1.0, 1.0),
):
    """
    set_common_shader_uniforms

    :param line_color: tuple(float, float, float)
    :param highlight_color: tuple(float, float, float)
    :param shader: QOpenGLShaderProgram
    :param point_size: float = 10.0
    :param highlight: bool = False
    :return: None

    Sets all common uniforms used in shared src.

    - Uses OpenGL directly (not Qt wrappers).
    - Assumes shader_manager.current_shader_program is already bound.
    """

    def safe_set_matrix(name: bytes, mat: np.ndarray):
        loc = shader.uniformLocation(name)
        if loc >= 0:
            set_uniform_matrix(shader, name, mat)

    def safe_set_float(name: bytes, val: float):
        loc = shader.uniformLocation(name)
        if loc >= 0:
            set_uniform_float(shader, name, val)

    def safe_set_bool(name: bytes, val: bool):
        loc = shader.uniformLocation(name)
        if loc >= 0:
            set_uniform_bool(shader, name, val)

    def safe_set_vec3(name: bytes, val: tuple):
        loc = shader.uniformLocation(name)
        if loc >= 0:
            set_uniform_vec3(shader, name, val)

    safe_set_matrix(b"mvp_matrix", mvp)
    safe_set_float(b"u_base_point_size", point_size)
    safe_set_bool(b"useHighlight", highlight)
    safe_set_vec3(b"highlightColor", highlight_color)
    safe_set_vec3(b"lineColor", line_color)


def set_common_uniforms(
    shader: QOpenGLShaderProgram,
    mvp: np.ndarray,
    point_size: float = 10.0,
    highlight: bool = False,
    highlight_color: Tuple[float, float, float] = (1.0, 0.0, 0.0),
    line_color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
) -> None:
    """
    set_common_uniforms

    :param shader: QOpenGLShaderProgram
    :param mvp: np.ndarray
    :param point_size: float
    :param highlight: bool
    :param highlight_color: Tuple
    :param line_color: Tuple
    :return: None

    Sets all common uniforms used by molecular src
    """

    try:
        set_uniform_matrix(shader, b"mvp_matrix", mvp)
        set_uniform_float(shader, b"u_base_point_size", point_size)
        set_uniform_bool(shader, b"useHighlight", highlight)
        set_uniform_vec3(shader, b"highlightColor", highlight_color)
        set_uniform_vec3(shader, b"lineColor", line_color)
    except Exception as ex:
        log.warning(
            f"⚠️ Could not set one or more shader_manager.current_shader_program uniforms: {ex}"
        )
