"""
Demonstrating the use of textures in PicoGL

compare to tu02_texture_without_normal.py
"""
import os

from pyglm import glm

from examples.picogl_window import PicoGLWindow
from examples.texture_renderer import TextureObjectRenderer

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
GLSL_DIR = os.path.join(CURRENT_DIR, "glsl", "tu02")


class TextureWindow(PicoGLWindow):
    """ file with stubs for actions """
    def __init__(self, width, height, *args, **kwargs):
        super().__init__( width, height,*args, **kwargs)
        self.renderer = TextureObjectRenderer(self.context)

    def initializeGL(self):
        """Initial OpenGL configuration."""
        super().initializeGL()
        self.renderer.initialize_shaders()
        self.renderer.initialize_rendering_buffers()

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
