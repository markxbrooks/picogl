from OpenGL.raw.GL.VERSION.GL_2_0 import glUseProgram

from elmo.utils.shaderLoader import Shader


def bind_shader(shader: Shader = None) -> None:
    """
    bind_shader

    :param shader:
    :return: None
    Bind the shader program for rendering.
    """
    glUseProgram(shader.program)
