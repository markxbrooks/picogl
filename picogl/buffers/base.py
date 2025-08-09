"""
OpenGL Render Buffer Base Class
===============================

This module defines a dataclass for managing OpenGL render buffers, including
Vertex Array Objects (VAOs), Vertex Buffer Objects (VBOs), and associated metadata
such as index counts. It provides a unified structure for buffer management and
includes cleanup functionality to safely delete OpenGL resources.

Dependencies:
-------------
- numpy
- PyOpenGL
- elmo.gl (custom rendering state management)
- picogl (legacy and modern OpenGL buffer abstractions)

Classes:
--------

.. autoclass:: RenderBuffersBase
    :members:
    :undoc-members:

Attributes:
-----------
- `vao`: Optional[VertexArrayObject] — Modern VAO wrapper.
- `vbo`: Optional[LegacyVBO] — Legacy VBO wrapper.
- `index_count`: Optional[int] — Number of indices used for rendering.

Methods:
--------
- `delete`: Cleans up VAO and VBO handles and resets internal state.

Usage Example:
--------------

.. code-block:: python

    buffers = RenderBuffersBase()
    buffers.delete()  # Safely release OpenGL resources
"""


from dataclasses import dataclass, field
from typing import Optional

from picogl.backend.legacy.core.vertex.buffer.vertex import LegacyVBO
from picogl.backend.modern.core.vertex.array.object import VertexArrayObject



@dataclass
class RenderBuffersBase:
    """OpenGL render buffer base class"""

    vao: Optional[VertexArrayObject] = None
    vbo: Optional[LegacyVBO] = None
    index_count: Optional[int] = 0

    def delete(self):
        """delete to remove atoms_buffers"""
        self.vao.delete()
        self.vbo.delete()
        self.index_count = 0

