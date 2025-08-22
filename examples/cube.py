"""Minimal PicoGL Cube. Compare to tu_01_color_cube.py"""

from pathlib import Path
from typing import NoReturn
from examples.data.cube_data import g_color_buffer_data, g_vertex_buffer_data
from picogl.renderer import MeshData
from picogl.ui.backend.glut.window.object import ObjectWindow

GLSL_DIR = Path(__file__).parent / "glsl" / "tu01"


def main() -> NoReturn:
    """Set up the colored object data and show it"""
    data = MeshData.from_raw(vertices=g_vertex_buffer_data, colors=g_color_buffer_data)
    window = ObjectWindow(
        width=800, height=600, title="Cube window", data=data, glsl_dir=GLSL_DIR
    )
    window.initializeGL()
    window.run()


if __name__ == "__main__":
    main()
