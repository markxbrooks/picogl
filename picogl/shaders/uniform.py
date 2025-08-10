from OpenGL.GL import glGetUniformLocation


def get_uniform_location(shader, uniform_name: str) -> int:
    """
    get uniform location
    :param shader: PicoGL shader object
    :param uniform_name: string uniform name\
    :return: uniform location int
    """
    return glGetUniformLocation(shader.program, uniform_name)
