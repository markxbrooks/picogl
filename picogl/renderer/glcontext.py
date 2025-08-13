"""
GL Context Class
"""

from dataclasses import dataclass
from typing import Optional

from picogl.backend.modern.core.shader.shader import PicoGLShader


@dataclass
class GLContext:
    """
    Stores dynamic OpenGL-related state (VAO, shader, texture handles, etc.).
    Does NOT store raw vertex data.
    """
    vao: Optional[int] = None
    shader: Optional[PicoGLShader] = None
    texture_id: Optional[int] = None
    vertex_count: int = 0
