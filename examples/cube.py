"""Minimal PicoGL Cube. Compare to tu_01_color_cube.py"""
from pathlib import Path
"""
    from typing import NoReturn

    from examples.data.cube_data import g_color_buffer_data, g_vertex_buffer_data
    from picogl.renderer import MeshData
    from picogl.ui.backend.glut.window.colored_object import ColoredObjectWindow

    GLSL_DIR = Path(__file__).parent / "glsl" / "tu01"

    def main() -> NoReturn:
        data = MeshData.from_raw(vertices=g_vertex_buffer_data, colors=g_color_buffer_data)
        window = ColoredObjectWindow(
            width=800,
            height=600,
            title="Cube window",
            data=data,
            glsl_dir=str(GLSL_DIR),
        )
        window.initializeGL()
        window.run()

    if __name__ == "__main__":
        main()
"""

import os

from examples.data.cube_data import g_color_buffer_data, g_vertex_buffer_data
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
