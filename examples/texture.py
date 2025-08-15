"""
Demonstrating textures - compare to tu02_texture_without_normal.py
"""
import os

from examples import g_vertex_buffer_data, g_uv_buffer_data
from picogl.renderer import MeshData
from picogl.ui.backend.glut.window.texture import TextureWindow
from picogl.utils.reshape import float32_row

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    """set up the cube and draw it"""
    cube_data = MeshData.from_raw(vertices=g_vertex_buffer_data,
                                  uvs=g_uv_buffer_data)
    win = TextureWindow(width=800,
                        height=600,
                        title="texture window",
                        data=cube_data,
                        base_dir=BASE_DIR)
    win.initializeGL()
    win.run()
