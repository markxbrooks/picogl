"""
Initialize VBOs
"""

from elmo.gl.backend.legacy.entities.calpha.setup import setup_calpha_vbos
from elmo.gl.backend.legacy.primitives.ribbon.setup import setup_ribbons_vbos
from picogl.logger import Logger as log
from elmo.pdb.three_dimensions.molecule import Molecule3D
from elmo.gl.buffers.molecule.molecule import MolecularRenderBuffers


def initialize_vbos(
    mol3d_atomic_model: Molecule3D,
    render_buffers: MolecularRenderBuffers,
    chain_colors: dict,
) -> None:
    """
    initialize_vbos

    :param mol3d_atomic_model: Molecule3D
    :param render_buffers: MolecularRenderBuffers
    :param chain_colors: dict
    :return: None
    """
    try:
        setup_ribbons_vbos(
            mol3d=mol3d_atomic_model,
            render_buffers=render_buffers,
            chain_colors=chain_colors,
        )
        setup_calpha_vbos(
            mol3d=mol3d_atomic_model,
            render_buffers=render_buffers,
            chain_colors=chain_colors,
        )
    except Exception as ex:
        log.error(f"Failed to initialize VBOs: {ex}")
