"""Minimal PicoGL Teapot."""
import os
from picogl.ui.backend.glut.window.object_window import ObjectWindow

GLSL_DIR = os.path.join(os.path.dirname(__file__), "glsl", "teapot")

win = ObjectWindow(width=800,
                   height=600,
                   title="Newell Teapot",
                   object_file_name="data/teapot.obj",
                   glsl_dir=GLSL_DIR)
win.initializeGL()
win.run()
