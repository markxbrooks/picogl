from OpenGL.raw.GL.VERSION.GL_1_0 import GL_TRIANGLES
from picogl.renderer import RendererBase, GLContext, MeshData
from picogl.backend.modern.core.vertex.array.object import VertexArrayObject


class ObjectRenderer(RendererBase):
    """ Basic renderer class """

    def __init__(self,
                 context: GLContext,
                 data: MeshData,
                 base_dir: str):
        super().__init__()
        self.context, self.data = context, data
        self.base_dir = base_dir
        self.show_model = True

    def initialize_shaders(self):
        """Load and compile shaders."""
        self.context.create_shader_program(vertex_source_file="vertex.glsl",
                                            fragment_source_file="fragment.glsl",
                                            base_dir=self.base_dir)

    def initialize_buffers(self):
        """Create VAO and VBOs once."""
        if self.context.vaos is None:
            self.context.vaos = {}
        self.context.vaos["cube"] = cube_vao = VertexArrayObject()
        cube_vao.add_vbo(index=0, data=self.data.vbo, size=3)
        cube_vao.add_vbo(index=1, data=self.data.cbo, size=3)

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
        with self.context.shader, self.context.vaos["cube"]:
            self.context.shader.uniform("mvp_matrix", self.context.mvp_matrix)
            self.context.vaos["cube"].draw(mode=GL_TRIANGLES, index_count=self.data.vertex_count)
