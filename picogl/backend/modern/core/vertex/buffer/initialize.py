"""
Initialize VBOs
"""

from elmo.gl.backend.modern.entities.calpha.setup import setup_calpha_vaos
from elmo.gl.backend.modern.primitives.ribbon.setup import setup_ribbons_vaos
from picogl.logger import Logger as log
from elmo.pdb.three_dimensions.molecule import Molecule3D
from elmo.gl.buffers.molecule.molecule import MolecularRenderBuffers


def initialize_vaos(
    mol3d: Molecule3D, render_buffers: MolecularRenderBuffers, chain_colors: dict
) -> None:
    """
    initialize_vaos

    :param mol3d: Molecule3D
    :param render_buffers: MolecularRenderBuffers
    :param chain_colors: dict
    :return: None
    """
    try:
        setup_ribbons_vaos(
            mol3d=mol3d,
            chain_colors=chain_colors,
            ribbon_group=render_buffers.ribbons_modern,
        )
        setup_calpha_vaos(
            mol3d=mol3d,
            chain_colors=chain_colors,
            calpha=render_buffers.calpha,
        )
    except Exception as ex:
        log.error(f"Failed to initialize VBOs: {ex}")
