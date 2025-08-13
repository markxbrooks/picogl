"""
GL Context Class
"""

from dataclasses import dataclass, field
from typing import Optional

import numpy as np

from picogl.backend.modern.core.shader.program import ShaderProgram
from picogl.backend.modern.core.vertex.array.object import VertexArrayObject


@dataclass
class GLContext:
    """
    Stores dynamic OpenGL-related state (VAO, shader, texture handles, etc.).
    Does NOT store raw vertex data.
    """
    vaos: dict[str, VertexArrayObject] = field(default_factory=dict)
    vertex_array: Optional[VertexArrayObject] = None
    shader: Optional[ShaderProgram] = None
    texture_id: Optional[int] = None
    mvp_matrix: np.ndarray = field(default_factory=lambda: np.identity(4, dtype=np.float32))

    def create_shader_program(self, vertex_source_file: str,
                              fragment_source_file: str,
                              base_dir: str):
        """
        create_shader_program

        :param vertex_source_file: str
        :param fragment_source_file: str
        :param base_dir: str
        :return: None
        """
        self.shader = ShaderProgram(vertex_source_file=vertex_source_file,
                                    fragment_source_file=fragment_source_file,
                                    base_dir=base_dir)
