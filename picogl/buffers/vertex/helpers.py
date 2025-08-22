from picogl.buffers.vertex.abstract import VertexArrayGroup


def create_vertex_array_group(use_vao: bool) -> VertexArrayGroup:
    """
    create_vertex_array_group

    Small factory to pick backend (optional)
    """
    if use_vao:
        return ModernVertexArrayGroup()
    else:
        return LegacyVertexArrayGroup()