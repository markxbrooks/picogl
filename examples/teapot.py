"""Minimal PicoGL Teapot."""
import os

from examples.object_renderer import ObjectRenderer
from picogl.renderer import GLContext, MeshData
from picogl.ui.backend.glut.window.glut_renderer import GlutRendererWindow
from picogl.utils.normal import compute_vertex_normals, compute_normals_from_vbo
from picogl.utils.reshape import float32_row
from picogl.utils.loader.object import OBJLoader, ObjectData

GLSL_DIR = os.path.join(os.path.dirname(__file__), "glsl", "teapot")


class TeapotWindow(GlutRendererWindow):
    def __init__(self, width, height, *args, **kwargs):
        super().__init__(width, height, *args, **kwargs)
        self.context = GLContext()

        obj_loader = OBJLoader("data/teapot.obj")
        raw_data = obj_loader.to_array_style()

        # Ensure indices exist
        indices = getattr(raw_data, "indices", None)
        if indices is None:
            # If OBJ is already single-indexed, generate sequential indices
            indices = list(range(len(raw_data.vertices)//3))

        self.data = ObjectData(
            vertices=raw_data.vertices,
            texcoords=raw_data.texcoords or [],
            normals=raw_data.normals,
            indices=indices
        )

        self.renderer = ObjectRenderer(
            context=self.context,
            data=MeshData(
                vbo=float32_row(self.data.vertices),
                nbo=float32_row(self.data.normals),
                cbo=float32_row([[1.0, 0.0, 0.0]] * (len(self.data.vertices)//3))
            ),
            base_dir=GLSL_DIR
        )

win = TeapotWindow(width=800, height=600)
win.initializeGL()
win.run()