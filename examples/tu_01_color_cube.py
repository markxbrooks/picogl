# import os,sys
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import os
from typing import Any

import numpy as np

from OpenGL.GL import *  # pylint: disable=W0614
from pyglm import glm

from picogl.backend.modern.core.shader.shader import PicoGLShader
from picogl.backend.modern.core.vertex.buffer.object import ModernVBO
from picogl.shaders.mvp import calculate_mvp_matrix, set_mvp_matrix_to_uniform_id
from picogl.shaders.uniform import get_uniform_location
from picogl.logger import setup_logging, Logger as log
from utils.glutWindow import GlutWindow
from examples.data import g_vertex_buffer_data, g_color_buffer_data

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
GLSL_DIR = os.path.join(CURRENT_DIR, "glsl", "tu01")
setup_logging()


def to_float32_row(array_like: Any) -> np.ndarray:
    """
    Reshape input to a single row and convert to np.float32.

    :param array_like: Any array-like object (list, tuple, np.ndarray).
    :return: A NumPy array of shape (1, N) with dtype np.float32.
    """
    return np.reshape(array_like, (1, -1)).astype(np.float32)

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
        self.context.vbo = ModernVBO()
        self.context.vbo.bind()
        self.context.vbo.set_data(data=self.cube_data_positions)

        self.context.cbo = ModernVBO()
        self.context.cbo.bind()
        self.context.cbo.set_data(data=self.cube_color_data)

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

            glEnableVertexAttribArray(0)
            glBindBuffer(GL_ARRAY_BUFFER, self.context.vbo.handle)
            glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,None)

            glEnableVertexAttribArray(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.context.cbo.handle)
            glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,0,None)

            glDrawArrays(GL_TRIANGLES, 0, 12*3) # 12*3 indices starting at 0 -> 12 triangles

            glDisableVertexAttribArray(0)
            glDisableVertexAttribArray(1)


if __name__ == "__main__":

    win = CubeWindow()
    win.initializeGL()
    win.initialize_buffers()
    win.run()
