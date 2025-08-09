"""
setup_vao_colors
"""

from OpenGL.raw.GL.VERSION.GL_1_0 import GL_UNSIGNED_INT

from picogl.backend.modern.core.vertex.array.object import VertexArrayObject


def setup_vao_colors(vao: int, vbo: int, cbo: int, stride: int):
    """
    setup_vao_colors

    :param stride: int
    :param vao: int Vertex Array Object
    :param vbo: int Vertex Buffer Object for positions
    :param cbo: int Vertex Buffer Object for colors

    Configures the VAO for rendering.
    """
    with VertexArrayObject(vao) as vao_obj:
        vao_obj.add_attribute(index=0, vbo=vbo, dtype=GL_UNSIGNED_INT, stride=stride)  # Position
        vao_obj.add_attribute(index=1, vbo=cbo, dtype=GL_UNSIGNED_INT, stride=stride)  # Color


