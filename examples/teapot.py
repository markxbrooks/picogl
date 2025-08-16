"""Minimal PicoGL Teapot."""

import os
from pathlib import Path

from picogl.renderer import MeshData
from picogl.ui.backend.glut.window.object import ObjectWindow
from picogl.utils.loader.object import OBJLoader

GLSL_DIR = Path(__file__).parent / "glsl" / "teapot"


def main():
    """Set up the teapot object and show it."""
    object_file_name = "data/teapot.obj"
    obj_loader = OBJLoader(object_file_name)
    teapot_data = obj_loader.to_array_style()
    data = MeshData.from_raw(
        vertices=teapot_data.vertices,
        normals=teapot_data.normals,
        colors=([[1.0, 0.0, 0.0]] * (len(teapot_data.vertices) // 3))
    )
    win = ObjectWindow(
        width=800,
        height=600,
        title="Newell Teapot",
        glsl_dir=GLSL_DIR,
        data=data,
    )
    win.initializeGL()
    win.run()


if __name__ == "__main__":
    """Run the main function."""
    main()
