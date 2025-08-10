"""
Illustrating the use of PicoGL to draw a cube in OpenGL
"""

import os

from OpenGL.GL import *  # pylint: disable=W0614
from pyglm import glm

from picogl.backend.modern.core.shader.shader import PicoGLShader
from picogl.backend.modern.core.vertex.array.object import VertexArrayObject
from picogl.shaders.mvp import calculate_mvp_matrix, set_mvp_matrix_to_uniform_id
from picogl.shaders.uniform import get_uniform_location
from picogl.logger import setup_logging, Logger as log
from picogl.utils.reshape import to_float32_row
from utils.glutWindow import GlutWindow
from examples.data import g_vertex_buffer_data, g_color_buffer_data

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
GLSL_DIR = os.path.join(CURRENT_DIR, "glsl", "tu01")
setup_logging()


class CubeWindow(GlutWindow):

    class GLContext(object):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.cube_data_positions = to_float32_row(g_vertex_buffer_data)
        self.cube_color_data = to_float32_row(g_color_buffer_data)
        self.shader = None
        self.context = None

    def initializeGL(self):
        """
        initializeGL
        :return:
        """
        glClearColor(0.0,0,0.4,0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

    def initialize_buffers(self):
        """
        initialize_buffers
        """
        self.context = self.GLContext()
        self.shader = shader = PicoGLShader()

        shader.init_shader_from_glsl_files("vertex.glsl",
                                           "fragment.glsl",
                                           base_dir=GLSL_DIR)
        self.context.mvp_id = get_uniform_location(shader_program=shader.program,
                                                   uniform_name="mvp_matrix")

    def resizeGL(self, width: int, height: int):
        """
        resizeGL

        :param width: int
        :param height: int
        """
        glViewport(0, 0, width, height)
        calculate_mvp_matrix(self.context, width, height)

    def paintGL(self):
        """
        paintGL
        """
        log.message("paintGL")
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        with self.shader:
            set_mvp_matrix_to_uniform_id(self.context.mvp_id,
                                         self.context.mvp_matrix)
            cube_vao = VertexArrayObject()
            self.context.vertex_buffer_object = cube_vao.add_vbo(index=0, data=self.cube_data_positions, size=3)
            self.context.color_buffer_object = cube_vao.add_vbo(index=1, data=self.cube_color_data, size=3)
            with cube_vao:
                #cube_vao.draw(mode=GL_TRIANGLES, index_count=12 * 3)
                glDrawArrays(GL_TRIANGLES, 0, 12 * 3)


if __name__ == "__main__":

    win = CubeWindow()
    win.initializeGL()
    win.initialize_buffers()
    win.run()
