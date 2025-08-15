from examples import g_vertex_buffer_data, g_uv_buffer_data, TextureRenderer
from picogl.renderer import GLContext, MeshData
from picogl.ui.backend.glut.window.glut_renderer import GlutRendererWindow
from picogl.utils.reshape import float32_row


class TextureWindow(GlutRendererWindow):
    """file with stubs for actions"""
    def __init__(self, width, height, title, data, base_dir, *args, **kwargs):
        self.context = GLContext()
        self.base_dir = base_dir
        self.data = data
        super().__init__(width, height, title, context=self.context, *args, **kwargs)
        self.renderer = TextureRenderer(
            context=self.context,
            data=self.data,
            base_dir=self.base_dir
        )

    def initializeGL(self):
        """Initial OpenGL configuration."""
        super().initializeGL()
        self.renderer.initialize_shaders()
        self.renderer.initialize_buffers()

    def paintGL(self):
        """paintGL"""
        self.renderer.render()