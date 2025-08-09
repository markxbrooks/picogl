"""
Open GL shader_manager.current_shader_program compilation

Example Usage:
==============
>>>shader_manager.current_shader_program = qt_compile_shaders(DEFAULT_VERTEX_SHADER_SRC, DEFAULT_FRAGMENT_SHADER_SRC, shader_name)
...if shader_manager.current_shader_program:
...   shader_manager.current_shader_program.bind()

"""

from typing import Optional

from OpenGL.raw.GL.VERSION.GL_2_0 import (
    GL_COMPILE_STATUS,
    GL_FRAGMENT_SHADER,
    GL_VERTEX_SHADER,
    glGetShaderInfoLog,
)
from PySide6.QtOpenGL import QOpenGLShader, QOpenGLShaderProgram

from elmo.logger import Logger as log
from OpenGL.GL import glGetShaderiv
from OpenGL.GL.shaders import compileProgram
from picogl.shaders.load import DEFAULT_FRAGMENT_SHADER_SRC, DEFAULT_VERTEX_SHADER_SRC

VERTEX_SHADER_SRC_HARDCODED_TEST = """#version 330 core

layout(location = 0) in vec3 in_position;
layout(location = 1) in vec3 in_color;

uniform mat4 mvp_matrix;
uniform float u_base_point_size;

out vec3 frag_color;

void main() {
    gl_Position = mvp_matrix * vec4(in_position, 1.0);
    frag_color = in_color;
    gl_PointSize = u_base_point_size;
}
"""


def qt_compile_shaders(
    vertex_src: str, fragment_src: str, shader_name: Optional[str]
) -> Optional[QOpenGLShaderProgram]:
    """
    Compiles and links a vertex + fragment shader_manager.current_shader_program shader_program using Qt's OpenGL API.

    :param shader_name: str
    :param vertex_src: Vertex shader_manager.current_shader_program GLSL code.
    :param fragment_src: Fragment shader_manager.current_shader_program GLSL code.
    :return: Linked QOpenGLShaderProgram or None on failure.
    """
    program = QOpenGLShaderProgram()
    if not program.addShaderFromSourceCode(QOpenGLShader.Vertex, vertex_src):
        # if not shader_program.addShaderFromSourceCode(QOpenGLShader.Vertex, DEFAULT_VERTEX_SHADER_SRC):
        log.error(f"❌ Vertex Shader {shader_name} Compilation Failed")
        _log_shader_preview(vertex_src, fragment_src)
        log.error(program.log())
        return None

    if not program.addShaderFromSourceCode(QOpenGLShader.Fragment, fragment_src):
        # if not shader_program.addShaderFromSourceCode(QOpenGLShader.Fragment, DEFAULT_FRAGMENT_SHADER_SRC):
        log.error(f"❌ Fragment Shader {shader_name} Compilation Failed")
        _log_shader_preview(vertex_src, fragment_src)
        log.error(program.log())
        return None

    if not program.link():
        log.error("❌ Shader Program Linking Failed")
        _log_shader_preview(vertex_src, fragment_src)
        log.error(program.log())
        return None

    log.message(
        f"✅ Shader Program {shader_name} compiled (ID: {int(program.programId())})"
    )
    return program


def _log_shader_preview(vertex_src: str, fragment_src: str, preview_len: int = 200):
    """
    _log_shader_preview

    :param vertex_src: str
    :param fragment_src: str
    :param preview_len: int
    :return:
    """
    log.message(f"📄 Vertex Shader Preview:\n{vertex_src[:preview_len]}...")
    log.message(f"📄 Fragment Shader Preview:\n{fragment_src[:preview_len]}...")


def qt_compile_shaders_old(
    vertex_src: str, fragment_src: str
) -> Optional[QOpenGLShaderProgram]:
    """
    Compile and link vertex and fragment src using Qt's QOpenGLShaderProgram API.

    :param vertex_src: GLSL vertex shader_manager.current_shader_program source code as a string.
    :param fragment_src: GLSL fragment shader_manager.current_shader_program source code as a string.
    :return: Compiled and linked QOpenGLShaderProgram, or None on failure.
    """
    try:
        program = QOpenGLShaderProgram()
        log.parameter("vertex_src", vertex_src)
        log.parameter("fragment_src", fragment_src)
        if not program.addShaderFromSourceCode(QOpenGLShader.Vertex, vertex_src):
            log.message("❌ Vertex Qt Shader Compilation Failed:")
            log.message(f"📄 Vertex Shader Preview:\n{vertex_src[:200]}...")
            log.message(f"📄 Fragment Shader Preview:\n{fragment_src[:200]}...")
            log.error(program.log())
            return None

        if not program.addShaderFromSourceCode(QOpenGLShader.Fragment, fragment_src):
            log.error("❌ Fragment Shader Compilation Failed:")
            log.message(f"📄 Vertex Shader Preview:\n{vertex_src[:200]}...")
            log.message(f"📄 Fragment Shader Preview:\n{fragment_src[:200]}...")
            log.error(program.log())
            return None

        if not program.link():
            log.error("❌ Shader Program Linking Failed:")
            log.message(f"📄 Vertex Shader Preview:\n{vertex_src[:200]}...")
            log.message(f"📄 Fragment Shader Preview:\n{fragment_src[:200]}...")
            log.error(program.log())
            return None

        log.message(f"✅ Qt Shader Program created: {int(program.programId())}")
        return program
    except Exception as ex:
        log.error(
            f"Error {ex} occurred compiling shader_manager.current_shader_program shader_program."
        )


def compile_shaders() -> Optional[int]:
    """
    compile_shaders

    :return: Optional[int] shader_manager.current_shader_program
    """
    try:
        # Compile vertex and fragment src
        vertex_shader = compileShader(DEFAULT_VERTEX_SHADER_SRC, GL_VERTEX_SHADER)
        fragment_shader = compileShader(DEFAULT_FRAGMENT_SHADER_SRC, GL_FRAGMENT_SHADER)

        # Link them into a shader_program
        shader_program = compileProgram(vertex_shader, fragment_shader)

        # Optionally, check shader_manager.current_shader_program compile status
        for shader, name in [(vertex_shader, "Vertex"), (fragment_shader, "Fragment")]:
            status = glGetShaderiv(shader, GL_COMPILE_STATUS)
            if not status:
                log.error(
                    f"❌ {name} Shader Compile Error:\n{glGetShaderInfoLog(shader).decode()}"
                )

        log.message(f"✅ Shader shader_program created: {shader_program}")
        return shader_program

    except RuntimeError as e:
        log.error(f"❌ Shader compilation/linking failed:\n{e}")
        return None
