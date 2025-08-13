from OpenGL.raw.GL.VERSION.GL_1_0 import GL_TRIANGLES

from examples.data import g_vertex_buffer_data, g_color_buffer_data
from picogl.backend.modern.core.vertex.array.object import VertexArrayObject
from picogl.logger import Logger as log
from picogl.renderer.base import RendererBase
from picogl.shaders.mvp import set_mvp_matrix_to_uniform_id
from picogl.utils.reshape import to_float32_row


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
        from examples.cube import GLSL_DIR
        from picogl.backend.modern.core.shader.shader import PicoGLShader
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
            self.context.shader.uniform("mvp_matrix", self.context.mvp_matrix)
            self.context.cube_vao.draw(mode=GL_TRIANGLES, index_count=self.context.vertex_count)
