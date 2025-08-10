import os

from OpenGL import GL as gl

from picogl.logger import Logger as log


def log_gl_error():
    """
    log_gl_error
    """
    err = gl.glGetError() # pylint: disable=E1111
    if err != gl.GL_NO_ERROR:
        log.error(f'GL ERROR: {gl.gluErrorString(err)}') # pylint: disable=E1101


def compile_shader(program: int, shader: int, shader_source_list: str):
    """
    compile_shader

    :param program: int
    :param shader: int
    :param shader_source_list: list
    """
    gl.glShaderSource(shader, shader_source_list)
    gl.glCompileShader(shader)
    if gl.GL_TRUE != gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS):
        err = gl.glGetShaderInfoLog(shader)
        raise Exception(err)
    gl.glAttachShader(program, shader)


def read_shader_sources(shader_paths: list) -> list:
    """
    read_shader_sources
    :param shader_paths: list

    Read shader source from shader_paths
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sources = []
    for path in shader_paths:
        abs_path = os.path.join(base_dir, path)
        with open(abs_path, 'rb') as f:
            sources.append(f.read())
    return sources