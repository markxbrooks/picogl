"""Minimal PicoGL Cube. Compare to tu_01_color_cube.py"""

import os

from examples.data import g_color_buffer_data, g_vertex_buffer_data
from picogl.renderer import MeshData
from picogl.ui.backend.glut.window.colored_object import ColoredObjectWindow

GLSL_DIR = os.path.join(os.path.dirname(__file__), "glsl", "tu01")

if __name__ == "__main__":
    # Set up the colored object dat and show it
    data = MeshData.from_raw(vertices=g_vertex_buffer_data, colors=g_color_buffer_data)
    window = ColoredObjectWindow(
        width=800, height=600, title="Cube window", data=data, glsl_dir=GLSL_DIR
    )
    window.initializeGL()
    window.run()
