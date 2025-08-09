"""
AbstractBufferFactory
"""

from elmo.pdb.three_dimensions.atom import Atom3D
from elmo.gl.buffers.molecule.atom import AtomBufferGroup
from elmo.gl.buffers.molecule.bond import BondBufferGroup
from elmo.gl.buffers.molecule.calpha import CalphaBufferGroup


class AbstractBufferFactory:
    def create_atom_buffers(self, atoms: list[Atom3D]) -> AtomBufferGroup:
        """
        create_atom_buffers
        :return: None
        """
        raise NotImplementedError("Should be implemented in subclass")

    def create_bond_buffers(
        self, atoms: list[Atom3D], bond_color=(0.6, 0.6, 0.6)
    ) -> BondBufferGroup | None:
        """
        create_bond_buffers

        :param atoms: list of atoms
        :param bond_color: tuple(float, float, float)
        :return: BondBufferGroup
        """
        raise NotImplementedError("Should be implemented in subclass")

    def create_calpha_buffers(
        self, atoms: list[Atom3D], chain_colors: dict
    ) -> CalphaBufferGroup | None:
        """
        create_calpha_buffers

        :param atoms: list[Atom3D]
        :param chain_colors:  dict
        :return: CalphaBufferGroup
        """
        raise NotImplementedError("Should be implemented in subclass")
