from pyglm import glm
from OpenGL.raw.GL.VERSION.GL_1_0 import GL_TRIANGLES

from examples.data import g_vertex_buffer_data, g_uv_buffer_data
from examples.utils.textureLoader import textureLoader
from picogl.backend.modern.core.shader.shader import PicoGLShader
from picogl.backend.modern.core.uniform import set_uniform_location_value
from picogl.backend.modern.core.vertex.array.object import VertexArrayObject
from picogl.logger import Logger as log
from picogl.renderer.base import RendererBase
from picogl.shaders.mvp import set_mvp_matrix_to_uniform_id
from picogl.utils.gl_init import execute_gl_tasks, paintgl_list
from picogl.utils.reshape import to_float32_row
from picogl.utils.texture import bind_texture_array


class TextureObjectRenderer(RendererBase):
    """ Basic renderer class """
    def __init__(self, context):
        super().__init__()
        self.context = context
        self.show_model = True
        self.context.cube_data_positions = to_float32_row(g_vertex_buffer_data)
        self.context.uv_buffer_data = to_float32_row(g_uv_buffer_data)
        self.context.vertex_count = len(self.context.cube_data_positions.flatten()) // 3

    def initialize_shaders(self):
        """Load and compile shaders."""
        log.message("Loading shaders...")
        from examples.texture import GLSL_DIR
        self.context.shader = shader = PicoGLShader(vertex_source_file="vertex.glsl",
                                   fragment_source_file="fragment.glsl",
                                   base_dir=GLSL_DIR)
        self.context.texture_id =  shader.get_uniform_location("myTextureSampler")
        self.context.mvp_id = shader.get_uniform_location(uniform_name="mvp_matrix")
        log.parameter("MVP uniform ID: ", self.context.mvp_id)

    def initialize_rendering_buffers(self):
        """initialize buffers"""
        texture = textureLoader("resources/tu02/uvtemplate.tga")
        self.context.texture_glid = texture.textureGLID
        if texture.inversedVCoords:
            for index in range(0,len(g_uv_buffer_data)):
                if index % 2:
                    g_uv_buffer_data[index] = 1.0 - g_uv_buffer_data[index]
        self.context.cube_vao = VertexArrayObject()
        self.context.cube_vao.add_vbo(index=0, data=self.context.cube_data_positions, size=3)
        self.context.cube_vao.add_vbo(index=1, data=self.context.uv_buffer_data, size=2)

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
        execute_gl_tasks(paintgl_list)
        with self.context.shader, self.context.cube_vao:
            set_mvp_matrix_to_uniform_id(self.context.mvp_id, self.context.mvp_matrix)
            bind_texture_array(self.context.texture_glid)
            set_uniform_location_value(self.context.texture_id, 0)
            self.context.cube_vao.draw(mode=GL_TRIANGLES, index_count=self.context.vertex_count)
