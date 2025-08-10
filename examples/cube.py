import os, sys
import numpy as np

from OpenGL.GL import *  # pylint: disable=W0614
from pyglm import glm

from picogl.backend.modern.core.vertex.array.object import VertexArrayObject
from picogl.backend.modern.core.vertex.buffer.object import ModernVBO
from picogl.backend.modern.core.shader.shader import PicoGLShader
from picogl.shaders.uniform import get_uniform_location
from picogl.utils.glut import GlutWindow
from picogl.logger import setup_logging, Logger as log
from examples.data import g_vertex_buffer_data, g_color_buffer_data

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

setup_logging()


def calculate_mvp_matrix(context, width: int = 1920,
                         height: int = 1080) -> None:
    """
    calculate_mvp_matrix

    :param context: GLContext
    :param width: int
    :param height: int
    :return: None
    """
    context.projection = glm.perspective(glm.radians(45.0), float(width) / float(height), 0.1, 1000.0)
    context.view = glm.lookAt(glm.vec3(4, 3, -3),  # Camera is at (4,3,-3), in World Space
                              glm.vec3(0, 0, 0),  # and looks at the (0.0.0))
                              glm.vec3(0, 1, 0))  # Head is up (set to 0,-1,0 to look upside-down)
    context.model = glm.mat4(1.0)
    context.mvp_matrix = context.projection * context.view * context.model


class CubeWindow(GlutWindow):
    class GLContext(object):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.cube_data = None
        self.cube_color_data = None
        self.context = None
        self.shader = None

    def init_context(self):
        """ init context """
        self.context = self.GLContext()
        self.shader = PicoGLShader()
        self.shader.init_shader_from_glsl_files("glsl/cube/vertex.glsl", "glsl/cube/fragment.glsl",
                                                base_dir=CURRENT_DIR)
        self.context.mvp_id = get_uniform_location(self.shader, "mvp_matrix")
        self.cube_data = np.reshape(g_vertex_buffer_data, (1, -1)).astype(np.float32)
        self.cube_color_data = np.reshape(g_color_buffer_data, (1, -1)).astype(np.float32)

    def initializeGL(self):
        """
        initializeGL
        """
        glClearColor(0.0, 0, 0.4, 0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

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
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        with self.shader:
            glUniformMatrix4fv(self.context.mvp_id, 1, GL_FALSE, glm.value_ptr(self.context.mvp_matrix))
            cube_vao = VertexArrayObject()
            self.context.vertex_buffer_object = cube_vao.add_vbo(index=0, data=self.cube_data, size=3)
            self.context.color_buffer_object = cube_vao.add_vbo(index=1, data=self.cube_color_data, size=3)
            with cube_vao:
                glDrawArrays(GL_TRIANGLES, 0, 12 * 3)


if __name__ == "__main__":
    win = CubeWindow()
    win.initializeGL()
    win.init_context()
    win.run()
