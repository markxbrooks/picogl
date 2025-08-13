"""
GLContext class
"""

import numpy as np


class GLData:
    """Holds OpenGL-related state objects for rendering."""
    def __init__(self,
                 positions: np.ndarray = None,
                 uv_buffers: np.ndarray = None,
                 colors: np.ndarray = None,):
        """ set up the OpenGL context """
        self.vertex_count = None
        self.positions = positions
        self.uv_buffers = uv_buffers
        self.colors = colors
        self.vertex_count = len(positions.flatten()) // 3 if positions is not None else None

    def __str__(self):
        return f"{self.positions} {self.uv_buffers} {self.colors} "
