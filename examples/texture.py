"""
Demonstrating textures - compare to tu02_texture_without_normal.py
"""

"""
from examples import g_vertex_buffer_data, g_uv_buffer_data
from picogl.renderer import MeshData
from picogl.ui.backend.glut.window.texture import TextureWindow

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GLSL_DIR = os.path.join(BASE_DIR, "glsl", "tu02")

if __name__ == "__main__":
    # set up the cube and draw it
    cube_data = MeshData.from_raw(vertices=g_vertex_buffer_data, uvs=g_uv_buffer_data)
    win = TextureWindow(
        width=800,
        height=600,
        title="texture window",
        data=cube_data,
        base_dir=BASE_DIR,
        glsl_dir=GLSL_DIR,
    )
    win.initializeGL()
    win.run()
    
"""

from pathlib import Path
from typing import NoReturn

from examples import g_vertex_buffer_data, g_uv_buffer_data
from picogl.renderer import MeshData
from picogl.ui.backend.glut.window.texture import TextureWindow

BASE_DIR = Path(__file__).resolve().parent
GLSL_DIR = BASE_DIR / "glsl" / "tu02"


def main() -> NoReturn:
    """Set up the cube and draw it with texture."""
    cube_data = MeshData.from_raw(vertices=g_vertex_buffer_data, uvs=g_uv_buffer_data)
    win = TextureWindow(
        width=800,
        height=600,
        title="texture window",
        data=cube_data,
        base_dir=str(BASE_DIR),
        glsl_dir=str(GLSL_DIR),
    )
    win.initializeGL()
    win.run()


if __name__ == "__main__":
    main()
