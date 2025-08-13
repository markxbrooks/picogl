"""Minimal PicoGL Cube. Compare to tu_01_color_cube.py"""
import os
from picogl.renderer import GLContext, GLData
from picogl.utils.reshape import float32_row
from examples.object_renderer import ObjectRenderer
from examples.picogl_window import PicoGLWindow
from examples.data import g_vertex_buffer_data, g_color_buffer_data
GLSL_DIR = os.path.join(os.path.dirname(__file__), "glsl", "tu01")

class CubeWindow(PicoGLWindow):
    def __init__(self, width, height, *args, **kwargs):
        super().__init__(width, height, *args, **kwargs)
        self.context = GLContext()
        self.data = GLData(
            positions=float32_row(g_vertex_buffer_data),
            colors=float32_row(g_color_buffer_data),
        )
        self.renderer = ObjectRenderer(
            context=self.context,
            data=self.data,
            base_dir=GLSL_DIR
        )
        self.renderer.show_model = True  # set here whether to show the cube

win = CubeWindow(width=800, height=600)
win.initializeGL()
win.run()