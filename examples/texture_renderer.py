""" Texture Renderer class """
from OpenGL.raw.GL.VERSION.GL_1_0 import GL_TRIANGLES

from picogl.backend.modern.core.vertex.array.object import VertexArrayObject
from picogl.logger import Logger as log
from picogl.renderer import RendererBase, MeshData, GLContext
from picogl.utils.gl_init import execute_gl_tasks, paintgl_list
from picogl.utils.texture import bind_texture_array
from examples import g_uv_buffer_data
from examples.utils.textureLoader import textureLoader


class TextureRenderer(RendererBase):
    """Basic renderer class"""

    def __init__(self, context: GLContext, data: MeshData, base_dir: str = None):
        super().__init__()
        self.context = context
        self.data = data
        self.data.vertex_count = len(self.data.vbo.flatten()) // 3
        self.show_model = True
        self.base_dir = base_dir

    def initialize_shaders(self):
        """Load and compile shaders."""
        log.message("Loading shaders...")
        self.context.create_shader_program(vertex_source_file="vertex.glsl",
                                            fragment_source_file="fragment.glsl",
                                            base_dir=self.base_dir)

    def initialize_buffers(self):
        """initialize buffers"""
        texture = textureLoader("resources/tu02/uvtemplate.tga")
        self.context.texture_id = texture.textureGLID
        if texture.inversedVCoords:
            for index, _ in enumerate(g_uv_buffer_data):
                if index % 2:
                    g_uv_buffer_data[index] = 1.0 - g_uv_buffer_data[index]
        self.context.vertex_array = VertexArrayObject()
        self.context.vertex_array.add_vbo(index=0, data=self.data.vbo, size=3)
        self.context.vertex_array.add_vbo(index=1, data=self.data.uvs, size=2)

    def render(self) -> None:
        """render/dispatcher"""
        if self.show_model:
            self._draw_model()
        # Add more conditions and corresponding draw functions as needed
        self._finalize_render()

    def _draw_model(self):
        """Draw the model"""
        execute_gl_tasks(paintgl_list)
        with self.context.shader, self.context.vertex_array:
            self.context.shader.uniform("mvp_matrix", self.context.mvp_matrix)
            bind_texture_array(self.context.texture_id)
            self.context.shader.uniform("myTextureSampler", 0)
            self.context.vertex_array.draw(
                mode=GL_TRIANGLES, index_count=self.data.vertex_count
            )

    def _draw_selection(self):
        """Draw selection"""
