from OpenGL.raw.GL.VERSION.GL_1_0 import GL_TRIANGLES

from picogl.renderer.glcontext import GLContext
from picogl.renderer.gldata import GLData
from picogl.backend.modern.core.vertex.array.object import VertexArrayObject
from picogl.logger import Logger as log
from picogl.renderer.base import RendererBase


class BasicObjectRenderer(RendererBase):
    """ Basic renderer class """

    def __init__(self,
                 context: GLContext,
                 data: GLData,
                 base_dir: str):
        super().__init__()
        self.context = context
        self.data = data
        self.data.vertex_count = len(self.data.positions.flatten()) // 3
        self.base_dir = base_dir

    def initialize_shaders(self):
        """Load and compile shaders."""
        log.message("Loading shaders...")
        from picogl.backend.modern.core.shader.shader import PicoGLShader
        self.context.shader = PicoGLShader(vertex_source_file="vertex.glsl",
                                           fragment_source_file="fragment.glsl",
                                           base_dir=self.base_dir)
        self.context.mvp_id = self.context.shader.get_uniform_location(uniform_name="mvp_matrix")
        log.parameter("MVP uniform ID: ", self.context.mvp_id)

    def initialize_buffers(self):
        """Create VAO and VBOs once."""
        log.message("Creating VAO and VBOs...")
        cube_vao = VertexArrayObject()
        cube_vao.add_vbo(index=0, data=self.data.positions, size=3)
        cube_vao.add_vbo(index=1, data=self.data.colors, size=3)
        self.context.vertex_array = cube_vao
        log.message(f"Buffers initialized with {self.data.vertex_count} vertices.")

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
        with self.context.shader, self.context.vertex_array:
            self.context.shader.uniform("mvp_matrix", self.context.mvp_matrix)
            self.context.vertex_array.draw(mode=GL_TRIANGLES, index_count=self.data.vertex_count)
