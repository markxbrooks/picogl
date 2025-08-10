
import os
from OpenGL import GL as gl


from picogl.backend.modern.core.shader.shader_helpers import log_gl_error, read_shader_source
from picogl.logger import Logger as log


def compile_shader(shader_program: int,
                   shader_type: int,
                   source: str):
    """
    compile_vertex_shader

    :param shader_program: int shader program
    :param shader_type: int shader type e.g. GL_VERTEX_SHADER GL_FRAGMENT_SHADER
    :param source: shader source string
    """
    shader = gl.glCreateShader(shader_type)  # pylint: disable=E1111
    gl.glShaderSource(shader, source)
    gl.glCompileShader(shader)
    if gl.GL_TRUE != gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS):
        err = gl.glGetShaderInfoLog(shader)
        raise Exception(err)
    gl.glAttachShader(shader_program, shader)
    log_gl_error()
    return shader


class PicoGLShader:
    """OpenGL Shader program manager for vertex and fragment shaders."""

    def __init__(self,
                 shader_name: str = None,
                 vertex_source_file: str = None,
                 fragment_source_file: str = None,
                 base_dir: str = None):
        """ constructor """
        self.shader_name = shader_name
        self.vertex_source_file = vertex_source_file
        self.fragment_source_file = fragment_source_file
        self.base_dir = base_dir
        self.vertex_shader = None
        self.fragment_shader = None
        self.program = None

        if vertex_source_file is not None and vertex_source_file is not None:
            self.init_shader_from_glsl_files(vertex_source_file=vertex_source_file,
                                             fragment_source_file=fragment_source_file,
                                             base_dir=base_dir)

    def __enter__(self):
        self.bind()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unbind()

    def program_id(self):
        return self.program

    def init_shader_from_glsl_files(self,
                              vertex_source_file: str,
                              fragment_source_file: str,
                              base_dir: str = None) -> None:
        """
        init_shader_from_glsl_files

        :param base_dir: directory containing vertex shaders
        :param vertex_source_file: list of paths to vertex shaders
        :param fragment_source_file: list of paths to fragment shaders
        :return: None
        """
        vertex_sources = read_shader_source(vertex_source_file, base_dir=base_dir)
        fragment_sources = read_shader_source(fragment_source_file, base_dir=base_dir)
        self.init_shader_from_glsl(vertex_sources, fragment_sources)

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
        log.parameter("self.program", self.program)
        log.parameter("vertex_source", vertex_source)
        log.parameter("fragment_source", fragment_source)
        self.vertex_shader = compile_shader(self.program, gl.GL_VERTEX_SHADER, vertex_source)
        self.fragment_shader = compile_shader(self.program, gl.GL_FRAGMENT_SHADER, fragment_source)
        self.link_shader_program()

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
    
    def get_uniform_location(self, uniform_name):
        """get_uniform_location"""
        mvp_id = get_uniform_location(
        shader_program=self.program,
        uniform_name=uniform_name)
        return mvp_id

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

    def unbind(self):
        gl.glUseProgram(0)

    def release(self):
        gl.glUseProgram(0)
