"""
Binding OpenGL shaders
"""

from OpenGL.raw.GL.VERSION.GL_2_0 import glUseProgram
from PySide6.QtOpenGL import QOpenGLShaderProgram


def use_shader_program(shader_program: int) -> None:
    """
    use_shader_program

    :param shader_program: int
    :return: None
    """
    glUseProgram(shader_program)


def bind_shader_program(qt_shader_program: QOpenGLShaderProgram) -> None:
    """
    use_shader_program

    :param qt_shader_program: QOpenGLShaderProgram
    :return: None
    """
    qt_shader_program.bind()
