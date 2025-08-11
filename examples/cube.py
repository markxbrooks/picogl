"""
Illustrating the use of PicoGL to draw a cube in OpenGL

compare to tu_01_color_cube
"""

import os
from OpenGL.GL import *  # pylint: disable=W0614
from pyglm import glm

from examples.object_renderer import BasicObjectRenderer
from examples.picogl_window import PicoGLWindow

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
GLSL_DIR = os.path.join(CURRENT_DIR, "glsl", "tu01")


class CubeWindow(PicoGLWindow):

    class GLContext:
        """Holds OpenGL-related state objects."""
        pass

    def __init__(self, width, height, *args, **kwargs):
        super().__init__(width, height,*args, **kwargs)
        self.renderer = BasicObjectRenderer(self.context)
        self.renderer.show_model = True # set here whether or not to show the cube

    def initializeGL(self):
        """Initial OpenGL configuration."""
        super().initializeGL()
        self.renderer.initialize_shaders()
        self.renderer.initialize_rendering_buffers()

    def resizeGL(self, width: int, height: int):
        """Adjust viewport and recalculate MVP matrix."""
        super().resizeGL(width, height)

    def paintGL(self):
        """Render the scene."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
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
