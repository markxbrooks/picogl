"""
Illustrating the use of PicoGL to draw a cube in OpenGL

compare to tu_01_color_cube
"""

import os
from OpenGL.GL import *  # pylint: disable=W0614
from pyglm import glm

from picogl.backend.modern.core.shader.shader import PicoGLShader
from picogl.backend.modern.core.vertex.array.object import VertexArrayObject
from picogl.renderer.base import RendererBase
from picogl.shaders.mvp import calculate_mvp_matrix, set_mvp_matrix_to_uniform_id
from picogl.logger import setup_logging, Logger as log
from picogl.utils.gl_init import init_gl_context, gl_init_list
from picogl.utils.reshape import to_float32_row
from utils.glutWindow import GlutWindow
from examples.data import g_vertex_buffer_data, g_color_buffer_data

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
GLSL_DIR = os.path.join(CURRENT_DIR, "glsl", "tu01")

class BasicObjectRenderer(RendererBase):
    """ Basic renderer class """
    def __init__(self, context):
        super().__init__()
        self.context = context
        self.context.cube_data_positions = to_float32_row(g_vertex_buffer_data)
        self.context.cube_color_data = to_float32_row(g_color_buffer_data)
        self.context.vertex_count = len(self.context.cube_data_positions.flatten()) // 3

    def initialize_shaders(self):
        """Load and compile shaders."""
        log.message("Loading shaders...")
        self.context.shader = PicoGLShader(vertex_source_file="vertex.glsl",
                                   fragment_source_file="fragment.glsl",
                                   base_dir=GLSL_DIR)
        self.context.mvp_id = self.context.shader.get_uniform_location(uniform_name="mvp_matrix")
        log.parameter("MVP uniform ID: ", self.context.mvp_id)

    def initialize_rendering_buffers(self):
        """Create VAO and VBOs once."""
        log.message("Creating VAO and VBOs...")
        cube_vao = VertexArrayObject()
        cube_vao.add_vbo(index=0, data=self.context.cube_data_positions, size=3)
        cube_vao.add_vbo(index=1, data=self.context.cube_color_data, size=3)
        self.context.cube_vao = cube_vao
        log.message(f"Buffers initialized with {self.context.vertex_count} vertices.")

    def render(self) -> None:
        """
        render dispatcher
        :return: None
        """
        if self.show_model:
            self._draw_model()
        # Add more conditions and corresponding draw functions as needed
        self._finalize_render()

    def _draw_model(self):
        """Draw the model"""
        with self.context.shader, self.context.cube_vao:
            set_mvp_matrix_to_uniform_id(self.context.mvp_id, self.context.mvp_matrix)
            self.context.cube_vao.draw(mode=GL_TRIANGLES, index_count=self.context.vertex_count)

class CubeWindow(GlutWindow):

    class GLContext:
        """Holds OpenGL-related state objects."""
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.height = None
        self.width = None
        self.context = self.GLContext()
        self.renderer = BasicObjectRenderer(self.context)
        self.renderer.show_model = True # set here whether or not to show the cube
        # Mouse interaction state
        self.last_mouse_x = None
        self.last_mouse_y = None
        self.rotation_x = 0.0
        self.rotation_y = 0.0
        setup_logging()

    def update_mvp_matrix(self):
        """Base perspective matrix from your existing method"""
        width, height = self.get_size()
        calculate_mvp_matrix(self.context, width, height)

        # Apply rotations
        rotation_matrix = glm.rotate(glm.mat4(1.0), glm.radians(self.rotation_x), glm.vec3(1, 0, 0))
        rotation_matrix = glm.rotate(rotation_matrix, glm.radians(self.rotation_y), glm.vec3(0, 1, 0))
        self.context.mvp_matrix = self.context.mvp_matrix * rotation_matrix

        self.update()  # Trigger repaint

    def initializeGL(self):
        """Initial OpenGL configuration."""
        log.message("Initializing OpenGL context...")
        init_gl_context(gl_init_list)

    def resizeGL(self, width: int, height: int):
        """Adjust viewport and recalculate MVP matrix."""
        log.message(f"Resizing viewport to {width}x{height}...")
        self.width = width
        self.height = height
        glViewport(0, 0, width, height)
        calculate_mvp_matrix(self.context, width, height)

    def get_size(self):
        """ get size """
        return self.width, self.height

    def paintGL(self):
        """Render the scene."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.renderer.render()

    def update(self):
        """ repaint """
        self.paintGL()

    def on_mouse(self, button, state, x, y):
        """ on mouse """
        if state == 0:  # Mouse button pressed
            self.last_mouse_x = x
            self.last_mouse_y = y

    def on_mousemove(self, x, y):
        """ on mouse move """
        if self.last_mouse_x is not None and self.last_mouse_y is not None:
            dx = x - self.last_mouse_x
            dy = y - self.last_mouse_y

            # Adjust sensitivity as needed
            self.rotation_x += dy * 0.5
            self.rotation_y += dx * 0.5

            self.update_mvp_matrix()

        self.last_mouse_x = x
        self.last_mouse_y = y

    def run_app(self):
        """Encapsulates initialization before main loop."""
        self.initializeGL()
        self.renderer.initialize_shaders()
        self.renderer.initialize_rendering_buffers()
        self.run()


if __name__ == "__main__":
    win = CubeWindow()
    win.run_app()
