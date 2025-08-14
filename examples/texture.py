"""
Demonstrating textures - compare to tu02_texture_without_normal.py
"""

import os

from examples import TextureRenderer, g_uv_buffer_data, g_vertex_buffer_data
from picogl.renderer import GLContext, MeshData
from picogl.ui.backend.glut.window.glut_renderer import GlutRendererWindow
from picogl.utils.reshape import float32_row

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
GLSL_DIR = os.path.join(CURRENT_DIR, "glsl", "tu02")


class TextureWindow(GlutRendererWindow):
    """file with stubs for actions"""

    def __init__(self, width, height, *args, **kwargs):
        positions = float32_row(g_vertex_buffer_data)
        uv_buffers = float32_row(g_uv_buffer_data)
        self.context = GLContext()
        self.data = MeshData(vbo=positions, uvs=uv_buffers)
        print(self.context)
        print(self.data)

        super().__init__(width, height, *args, **kwargs)
        self.renderer = TextureRenderer(
            context=self.context, data=self.data, base_dir=GLSL_DIR
        )

    def initializeGL(self):
        """Initial OpenGL configuration."""
        super().initializeGL()
        self.renderer.initialize_shaders()
        self.renderer.initialize_buffers()

    def resizeGL(self, width: int, height: int):
        """resizeGL"""
        super().resizeGL(width, height)

    def paintGL(self):
        """paintGL"""
        self.renderer.render()


if __name__ == "__main__":
    win = TextureWindow(width=800, height=600)
    win.initializeGL()
    win.run()
