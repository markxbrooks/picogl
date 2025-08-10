
import os
from OpenGL import GL as gl

from picogl.backend.modern.core.shader.shader_helpers import log_gl_error, compile_shader, read_shader_sources
from picogl.logger import Logger as log


class PicoGLShader:
    """OpenGL Shader program manager for vertex and fragment shaders."""

    def __init__(self, shader_name: str = None):
        """ constructor """
        self.shader_name = shader_name
        self.vertex_shader = None
        self.fragment_shader = None
        self.program = None

    def program_id(self):
        return self.program

    def init_shader_from_glsl(self,
                              vertex_source: str,
                              fragment_source: str) -> None:
        """
        init_shader_from_glsl

        :param vertex_source: list of paths to vertex shaders
        :param fragment_source: list of paths to fragment shaders
        :return: None
        """
        self.init_shader(vertex_source, fragment_source)

    def init_shader(self,
                    vertex_source: str,
                    fragment_source: str):
        """
        init_shader

        :param vertex_source: list of paths to vertex shaders
        :param fragment_source: list of paths to fragment shaders
        :return: None

        Create, compile, and link shaders into a program.
        """
        self.create_shader_program()
        self.vertex_shader = self._compile_shader(gl.GL_VERTEX_SHADER, vertex_source)
        self.fragment_shader = self._compile_shader(gl.GL_FRAGMENT_SHADER, fragment_source)
        self.link_shader_program()

    def _compile_shader(self,
                        shader_type,
                        source: str):
        """
        compile_vertex_shader

        :param shader_type: shader type
        :param source: list of paths to shader sources
        """
        shader = gl.glCreateShader(shader_type)
        compile_shader(self.program, shader, source)
        log_gl_error()
        return shader

    def create_shader_program(self):
        """
        create_shader_program
        """
        self.program = gl.glCreateProgram()
        log.message('Created shader program', self.program)
        log_gl_error()

    def link_shader_program(self):
        """
        link_shader_program
        """
        log.message('Linking shader program...')
        gl.glLinkProgram(self.program)
        if gl.GL_TRUE != gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS):
            err = gl.glGetProgramInfoLog(self.program)
            raise RuntimeError(f"Shader link failed: {err}")
        log_gl_error()

    def begin(self):
        """ begin"""
        gl.glUseProgram(self.program)
        log_gl_error()

    def end(self):
        """ end"""
        gl.glUseProgram(0)

    def bind(self):
        """ begin"""
        gl.glUseProgram(self.program)
        log_gl_error()

    def release(self):
        gl.glUseProgram(0)
