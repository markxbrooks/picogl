"""Minimal PicoGL Cube. Compare to tu_01_color_cube.py"""
import os

from examples.data import g_color_buffer_data, g_vertex_buffer_data
from picogl.renderer.object import ObjectRenderer
from picogl.renderer import GLContext, MeshData
from picogl.ui.backend.glut.window.glut_renderer import GlutRendererWindow
from picogl.utils.reshape import float32_row

GLSL_DIR = os.path.join(os.path.dirname(__file__), "glsl", "tu01")

class CubeWindow(GlutRendererWindow):
    """colored cube with no texture"""
    def __init__(self, width, height, title,  *args, **kwargs):
        super().__init__(width=width, height=height, title=title, *args, **kwargs)
        self.context = GLContext()
        self.data = MeshData(
            vbo=float32_row(g_vertex_buffer_data),
            cbo=float32_row(g_color_buffer_data),
        )
        self.renderer = ObjectRenderer(
            context=self.context,
            data=self.data,
            glsl_dir=GLSL_DIR
        )
        self.renderer.show_model = True  # set here whether to show the cube

win = CubeWindow(width=800, height=600,title = "cube window")
win.initializeGL()
win.run()
