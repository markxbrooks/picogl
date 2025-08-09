
"""
OpenGL Buffer Creation and Legacy Wrapper
=========================================

This module provides utilities for creating and managing OpenGL buffer objects,
including a simple function for uploading data to a buffer and a legacy-style
class wrapper for buffer operations. It supports both raw buffer creation and
object-oriented buffer management with bind/unbind and data upload methods.

Dependencies:
-------------
- numpy
- PyOpenGL

Functions:
----------

.. autofunction:: create_buffer
    Creates and uploads data to an OpenGL buffer. Returns the buffer handle.

Classes:
--------

.. autoclass:: LegacyBuffer
    :members:
    :undoc-members:

    A legacy-style wrapper for OpenGL buffer objects. Supports binding, unbinding,
    and setting data. Useful for maintaining compatibility with older rendering pipelines.

Attributes:
-----------
- `handle`: OpenGL buffer handle.
- `data`: NumPy array containing buffer data.
- `target`: OpenGL buffer target (e.g., GL_ARRAY_BUFFER).
- `index_count`: Number of elements in the buffer.

Usage Example:
--------------

.. code-block:: python

    # Using the function
    buffer = create_buffer(vertex_data)

    # Using the class
    legacy_buffer = LegacyBuffer(vertex_data)
    legacy_buffer.bind()
    legacy_buffer.set_data(new_data)
    legacy_buffer.unbind()
"""

import numpy as np
from OpenGL.raw.GL.VERSION.GL_1_5 import GL_ARRAY_BUFFER, GL_STATIC_DRAW, glBindBuffer

from OpenGL.GL import glBufferData, glGenBuffers


def create_vbo(data: np.ndarray, target: int = GL_ARRAY_BUFFER) -> int:
    """
    create_vbo

    :param data: np.ndarray containing buffer data.
    :param target: int e.g GL_ARRAY_BUFFER, or GL_ELEMENT_ARRAY_BUFFER
    :return: int
    Create and upload data to an OpenGL buffer
    Useful as a test function for maintaining compatibility with older rendering pipelines.
    """
    buf = glGenBuffers(1)
    glBindBuffer(target, buf)
    glBufferData(target, data.nbytes, data, GL_STATIC_DRAW)
    return buf


class LegacyBuffer:
    def __init__(
        self,
        data: np.ndarray,
        target: int = GL_ARRAY_BUFFER,
        mode: int = GL_STATIC_DRAW,
    ):
        """
        LegacyBuffer

        :param data: np.ndarray containing buffer data.
        :param target: int e.g GL_ARRAY_BUFFER, or GL_ELEMENT_ARRAY_BUFFER
        :return: int
        Create and upload data to an OpenGL buffer
        """
        self.handle = glGenBuffers(1)
        self.data = data
        self.target = target
        glBindBuffer(self.target, self.handle)
        self.set_data(data, target, mode)
        self.unbind()
        self.index_count = data.shape[0] if data.ndim > 0 else 0

    def bind(self):
        """Bind the buffer"""
        glBindBuffer(self.target, self.handle)

    def unbind(self):
        """Unbind the buffer"""
        glBindBuffer(self.target, 0)

    def set_data(
        self, data: np.ndarray, target: int = None, mode: int = GL_STATIC_DRAW
    ):
        """
        set_data
        Set data for the buffer
        :param data: np.ndarray containing buffer data.
        :param target: int e.g. GL_ARRAY_BUFFER, or GL_ELEMENT_ARRAY_BUFFER
        :param target:  GL_ARRAY_BUFFER, GL_ELEMENT_ARRAY_BUFFER, etc.
        :param mode: GL_STATIC_DRAW, GL_DYNAMIC_DRAW, etc.
        :return: None
        """
        glBufferData(target, data.nbytes, data, mode)
