"""
GLContext class
"""

import numpy as np


class MeshData:
    """Holds OpenGL-related state objects for rendering."""

    def __init__(
        self,
        vbo: np.ndarray = None,
        nbo: np.ndarray = None,
        uvs: np.ndarray = None,
        cbo: np.ndarray = None,
    ):
        """set up the OpenGL context"""
        self.vbo = vbo
        self.nbo = nbo
        self.uvs = uvs
        self.cbo = cbo
        self.vertex_count = len(vbo.flatten()) // 3 if vbo is not None else None

    def __str__(self):
        return f"{self.vbo} {self.uvs} {self.cbo} "
