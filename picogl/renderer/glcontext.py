"""
GL Context Class
"""

from dataclasses import dataclass, field
from typing import Optional

import numpy as np

from picogl.backend.modern.core.shader.program import PicoGLShader
from picogl.backend.modern.core.vertex.array.object import VertexArrayObject


@dataclass
class GLContext:
    """
    Stores dynamic OpenGL-related state (VAO, shader, texture handles, etc.).
    Does NOT store raw vertex data.
    """
    vertex_array: Optional[VertexArrayObject] = None
    shader: Optional[PicoGLShader] = None
    texture_id: Optional[int] = None
    mvp_matrix: np.ndarray = field(default_factory=lambda: np.identity(4, dtype=np.float32))
