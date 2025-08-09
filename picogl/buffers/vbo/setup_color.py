"""
OpenGL VBO Utilities for Molecular Coordinate and Color Data
=============================================================

This module provides utilities for creating and uploading Vertex Buffer Objects (VBOs)
for molecular visualization using modern OpenGL. It supports the creation of VBOs for
atom coordinate_data_main and per-vertex colors from parsed PDB data via BioPandas.

Functions
---------

- ``create_color_vbo``:
    Creates and uploads a VBO containing RGB color_array data for each vertex, suitable for use with shaders.

- ``create_vbo``:
    Parses atom coordinate_data_main from a `PandasPdb` structure and uploads them into a specified VBO.

Dependencies
------------

- `PyOpenGL` for OpenGL buffer operations.
- `NumPy` for efficient numeric data representation.
- `BioPandas` for reading and manipulating PDB data.
- `elmo.logger.Logger` for structured logging.
- `elmo.pdb.coordinate.parser.pdb_parse_for_vbo` for converting parsed PDB data to coordinate atoms_buffers.

Note
----

All functions assume that a valid OpenGL context is active. These utilities are intended for
use in applications rendering biomolecular structures with VAOs and shaders.

"""

import ctypes

import numpy as np
from OpenGL.raw.GL._types import GL_FALSE, GL_FLOAT
from OpenGL.raw.GL.VERSION.GL_1_5 import GL_ARRAY_BUFFER, GL_STATIC_DRAW, glBindBuffer
from OpenGL.raw.GL.VERSION.GL_2_0 import glEnableVertexAttribArray

from OpenGL.GL import glBufferData, glGenBuffers, glVertexAttribPointer

from picogl.backend.modern.core.vertex.buffer.object import ModernVBO


def setup_color_vbo(color_array: np.ndarray, location: int = 1) -> int:
    """
    setup_color_vbo

    :param color_array: np.ndarray Float32 data of shape (N, 3)
    :param location: int Attribute location in shader
    :return: int VBO handle
    """
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, color_array.nbytes, color_array, GL_STATIC_DRAW)
    glEnableVertexAttribArray(location)
    glVertexAttribPointer(location, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    return vbo


def setup_color_vbo_object(color_array: np.ndarray, location: int = 1) -> int:
    """
    setup_color_vbo_object

    :param color_array: np.ndarray Float32 data of shape (N, 3)
    :param location: int Attribute location in shader
    :return: int VBO handle
    """
    vbo_object = ModernVBO(data=color_array)
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, color_array.nbytes, color_array, GL_STATIC_DRAW)
    glEnableVertexAttribArray(location)
    glVertexAttribPointer(location, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    return vbo_object
