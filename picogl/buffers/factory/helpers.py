"""
Atom and Bond Buffer Preparation Utilities
==========================================

This module provides helper functions for generating vertex buffer data for atoms and bonds
in molecular visualization applications. It extracts positional and color data from `Atom3D`
objects and computes bond indices and associated rendering attributes.

Dependencies:
-------------
- numpy
- elmo.pdb.three_dimensions.atom (Atom3D)
- elmo.ui.colors (ColorMap)
- elmo.gl.backend.modern.entities.bonds.compute_indices
- elmo.logger (Logger)

Functions:
----------

.. autofunction:: prepare_atom_buffer_data
    Extracts position and color arrays from a list of `Atom3D` instances.

.. autofunction:: prepare_bond_buffer_data
    Computes bond indices and generates color, normal, and position arrays for rendering bonds.

Parameters:
-----------
- `atoms`: List of `Atom3D` objects representing molecular atoms.
- `bond_color`: RGB tuple used to color all bonds uniformly.

Returns:
--------
- `prepare_atom_buffer_data`: Tuple of NumPy arrays `(positions, colors)`.
- `prepare_bond_buffer_data`: Tuple of NumPy arrays `(bond_indices, colors, normals, positions)`.

Usage Example:
--------------

.. code-block:: python

    atom_positions, atom_colors = prepare_atom_buffer_data(atom_list)
    bond_indices, bond_colors, bond_normals, bond_positions = prepare_bond_buffer_data(atom_list, (0.8, 0.8, 0.8))
"""


from typing import Any

import numpy as np
from numpy import dtype, ndarray

from elmo.gl.backend.modern.entities.bonds.compute_indices import compute_bond_indices
from elmo.logger import Logger as log
from elmo.pdb.three_dimensions.atom import Atom3D
from elmo.ui.colors import ColorMap


def prepare_atom_buffer_data(atoms: list[Atom3D]) -> tuple[np.ndarray, np.ndarray]:
    """
    prepare_atom_buffer_data

    :param atoms: list[Atom3D]
    :return: tuple[np.ndarray, np.ndarray]
    Returns (positions, colors) arrays from Atom3D list.
    """
    positions = []
    colors = []
    for atom in atoms:
        x, y, z = atom.coords
        r, g, b = ColorMap.atom_colors.get(atom.element, (0.5, 0.5, 0.5))
        positions.extend([x, y, z])
        colors.extend([r, g, b])
    colors_array = np.array(colors, dtype=np.float32)
    log.parameter("colors_array", colors_array)
    return np.array(positions, dtype=np.float32), np.array(colors, dtype=np.float32)


def prepare_bond_buffer_data(
    atoms: list[Atom3D], bond_color: tuple[float, float, float]
) -> tuple[Any, ndarray[Any, dtype[Any]], ndarray[Any, dtype[Any]], ndarray]:
    """
    prepare_bond_buffer_data

    :param atoms: list[Atom3D] list of atoms
    :param bond_color: tuple[float, float, float] Color to show the bonds
    :return: tuple[ndarray, ndarray, ndarray, ndarray]
    """
    positions, _ = prepare_atom_buffer_data(atoms)
    points = positions.reshape(-1, 3)
    bond_indices = compute_bond_indices(points).astype(np.uint32)
    color_data = []
    for _ in bond_indices:
        color_data.extend(bond_color * 2)
    colors = np.array(color_data, dtype=np.float32)
    # Dummy normals: one per vertex, matching shape of positions
    normals = np.tile([0.0, 0.0, 1.0], (positions.shape[0], 1)).astype(np.float32)
    return bond_indices, colors, normals, positions
