"""Minimal PicoGL Teapot."""

import os
from picogl.ui.backend.glut.window.object import ObjectWindow

BASE_DIR = Path(__file__).resolve().parent
GLSL_DIR = BASE_DIR / "glsl" / "teapot"
# GLSL_DIR = os.path.join(os.path.dirname(__file__), "glsl", "teapot")


def main():
    """Set up the teapot object and show it."""
    win = ObjectWindow(
        width=800,
        height=600,
        title="Newell Teapot",
        object_file_name="data/teapot.obj",
        glsl_dir=str(GLSL_DIR),
    )
    win.initializeGL()
    win.run()


if __name__ == "__main__":
    """Run the main function."""
    main()
