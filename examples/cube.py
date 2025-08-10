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

    class GLContext:
        """Holds OpenGL-related state objects."""
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # ✅ Fixed super call
        self.cube_data_positions = to_float32_row(g_vertex_buffer_data)
        self.cube_color_data = to_float32_row(g_color_buffer_data)
        self.vertex_count = len(self.cube_data_positions.flatten()) // 3
        self.shader = None
        self.context = self.GLContext()

    # ------------------------------
    # Lifecycle Methods
    # ------------------------------

    def initializeGL(self):
        """Initial OpenGL configuration."""
        log.message("Initializing OpenGL context...")
        glClearColor(0.0, 0.0, 0.4, 0.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

    def initialize_shaders(self):
        """Load and compile shaders."""
        log.message("Loading shaders...")
        self.shader = PicoGLShader()
        self.shader.init_shader_from_glsl_files(
            "vertex.glsl", "fragment.glsl", base_dir=GLSL_DIR
        )
        self.context.mvp_id = get_uniform_location(
            shader_program=self.shader.program,
            uniform_name="mvp_matrix"
        )
        log.parameter("MVP uniform ID", self.context.mvp_id)

    def initialize_buffers(self):
        """Create VAO and VBOs once."""
        log.message("Creating VAO and VBOs...")
        cube_vao = VertexArrayObject()
        cube_vao.add_vbo(index=0, data=self.cube_data_positions, size=3)
        cube_vao.add_vbo(index=1, data=self.cube_color_data, size=3)
        self.context.cube_vao = cube_vao
        log.message(f"Buffers initialized with {self.vertex_count} vertices.")

    def resizeGL(self, width: int, height: int):
        """Adjust viewport and recalculate MVP matrix."""
        log.message(f"Resizing viewport to {width}x{height}...")
        glViewport(0, 0, width, height)
        calculate_mvp_matrix(self.context, width, height)

    def paintGL(self):
        """Render the scene."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        with self.shader, self.context.cube_vao:
            set_mvp_matrix_to_uniform_id(self.context.mvp_id, self.context.mvp_matrix)
            glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)

    # ------------------------------
    # Run Sequence
    # ------------------------------

    def run_app(self):
        """Encapsulates initialization before main loop."""
        self.initializeGL()
        self.initialize_shaders()
        self.initialize_buffers()
        self.run()


if __name__ == "__main__":
    win = CubeWindow()
    win.run_app()
