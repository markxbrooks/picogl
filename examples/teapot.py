"""Minimal PicoGL Teapot."""
import os
from examples.object_renderer import ObjectRenderer
from picogl.renderer import GLContext, MeshData
from picogl.ui.backend.glut.window.glut_renderer import GlutRendererWindow
from picogl.utils.loader.object import OBJLoader
GLSL_DIR = os.path.join(os.path.dirname(__file__), "glsl", "teapot")


class TeapotWindow(GlutRendererWindow):
    """ Teapot Object Window"""
    def __init__(self, width, height, title, *args, **kwargs):
        super().__init__(width, height, title, *args, **kwargs)
        self.context = GLContext()
        obj_loader = OBJLoader("data/teapot.obj")
        self.data = obj_loader.to_array_style()

        self.renderer = ObjectRenderer(
            context=self.context,
            data=MeshData.from_raw(
                vertices=self.data.vertices,
                normals=self.data.normals,
                colors=([[1.0, 0.0, 0.0]] * (len(self.data.vertices)//3))
            ),
            glsl_dir=GLSL_DIR
        )

win = TeapotWindow(width=800, height=600, title="Newell Teapot")
win.initializeGL()
win.run()
