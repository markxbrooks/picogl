"""
Illustrating the use of PicoGL to draw a cube in OpenGL

compare to tu_01_color_cube
"""

import os

from pyglm import glm

from examples.object_renderer import BasicObjectRenderer
from examples.picogl_window import PicoGLWindow
from picogl.renderer.glcontext import GLContext
from picogl.renderer.gldata import GLData
from picogl.utils.gl_init import execute_gl_tasks, paintgl_list
from examples.data import g_vertex_buffer_data, g_color_buffer_data
from picogl.utils.reshape import to_float32_row

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
GLSL_DIR = os.path.join(CURRENT_DIR, "glsl", "tu01")


class CubeWindow(PicoGLWindow):

    def __init__(self, width, height, *args, **kwargs):
        super().__init__(width, height,*args, **kwargs)
        self.context = GLContext()
        positions = to_float32_row(g_vertex_buffer_data)
        colors = to_float32_row(g_color_buffer_data)
        self.data = GLData(positions=positions,
                      colors=colors)
        self.renderer = BasicObjectRenderer(context=self.context,
                                            data=self.data,
                                            base_dir=GLSL_DIR)
        self.renderer.show_model = True # set here whether to show the cube

    def initializeGL(self):
        """Initial OpenGL configuration."""
        super().initializeGL()
        self.renderer.initialize_shaders()
        self.renderer.initialize_buffers()

    def resizeGL(self, width: int, height: int):
        """Adjust viewport and recalculate MVP matrix."""
        super().resizeGL(width, height)

    def paintGL(self):
        """Render the scene."""
        execute_gl_tasks(paintgl_list)
        self.renderer.render()

    def update(self):
        """ repaint """
        self.paintGL()

    def run_app(self):
        """Encapsulates initialization before main loop."""
        self.initializeGL()
        self.run()


if __name__ == "__main__":
    win = CubeWindow(width=800, height=600)
    win.run_app()
