import os

from OpenGL import GL as gl

from picogl.logger import Logger as log


def log_gl_error():
    """
    log_gl_error
    """
    err = gl.glGetError()  # pylint: disable=E1111
    if err != gl.GL_NO_ERROR:
        log.error(f"GL ERROR: {gl.gluErrorString(err)}")  # pylint: disable=E1101


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


def read_shader_source(shader_file_name: str, base_dir: str) -> str:
    """
    read_shader_source

    :param base_dir: str
    :param shader_file_name: str

    Read shader source from shader_paths
    """
    if not base_dir:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    abs_path = os.path.join(base_dir, shader_file_name)
    with open(abs_path, "r") as f:
        source = f.read()
    return source
