"""
LegacyVertexArrayGroup

Legacy backend (no real GL VAO support)
"""
import ctypes
from typing import Optional

from OpenGL.GL import glVertexAttribPointer
from OpenGL.raw.GL.VERSION.GL_1_0 import GL_POINTS, GL_TRIANGLES, GL_UNSIGNED_INT
from OpenGL.raw.GL.VERSION.GL_1_1 import (
    GL_COLOR_ARRAY,
    GL_NORMAL_ARRAY,
    GL_VERTEX_ARRAY,
    glDrawArrays, glDrawElements,
)
from OpenGL.raw.GL.VERSION.GL_1_5 import (
    GL_ARRAY_BUFFER,
    GL_ELEMENT_ARRAY_BUFFER,
    glBindBuffer,
)
from OpenGL.raw.GL.VERSION.GL_2_0 import (
    glDisableVertexAttribArray,
    glEnableVertexAttribArray,
)
from picogl.backend.legacy.core.vertex.buffer.client_states import legacy_client_states
from picogl.buffers.glcleanup import delete_buffer

from picogl.buffers.attributes import LayoutDescriptor
from picogl.buffers.vertex.abstract import VertexArrayGroup
from picogl.buffers.vertex.aliases import NAME_ALIASES


class LegacyVertexArrayGroup(VertexArrayGroup):
    """Container for legacy VBOs, mimicking VAO interface."""

    def __init__(self):
        self.index_count = 0
        self.handle = 0  # Does absolutely nothing
        self.vao = None  # Bonds Vertex Array Object. Does absolutely nothing
        self.vbo = None  # Atom Vertex Buffer Object
        self.cbo = None  # Color Vertex Buffer Object
        self.nbo = None  # Normal Vertex Buffer Object
        self.ebo = None  # Bond Index Buffer Object
        self.layout: Optional[LayoutDescriptor] = None
        self.vbos: dict[str, LegacyVBO] = {}  # store by semantic name

    def add_vbo(self, name: str, vbo: "LegacyVBO") -> "LegacyVBO":
        """Register a VBO by semantic name or shorthand alias."""
        # normalize to canonical key
        canonical = NAME_ALIASES.get(name, name)

        # store consistently
        self.vbos[canonical] = vbo

        # and assign to attribute if it exists
        if hasattr(self, canonical):
            setattr(self, canonical, vbo)

        return vbo

    def get_vbo(self, name: str) -> "LegacyVBO":
        """Retrieve a VBO by its semantic or shorthand name."""
        canonical = NAME_ALIASES.get(name, name)
        return self.vbos.get(canonical)

    def set_index_count(self, index: int):
        """Set the index count of the VBO."""
        self.index_count = index

    def delete(self) -> None:
        for buf in (self.nbo, self.cbo, self.vbo, self.ebo):
            if buf:
                delete_buffer(buf)
        self.nbo = self.cbo = self.vbo = self.ebo = None
        self.layout = None

    def draw(self, count: int = 0, mode=GL_POINTS):
        """
        draw

        :param count: int
        :param mode: int
        Enable legacy client states, bind VBOs, draw, and clean up.
        """

        if not count:
            count = self.index_count
        with self:
            with legacy_client_states(GL_VERTEX_ARRAY, GL_COLOR_ARRAY, GL_NORMAL_ARRAY):
                for vbo in self.vbos.values():
                    vbo.bind()
                # Issue draw call
                glDrawArrays(mode, 0, count)

    def draw_elements(
        self, count: int = 0, mode=GL_TRIANGLES, dtype=GL_UNSIGNED_INT, offset=0
    ):
        """
        Draw using an element buffer (EBO) with legacy client states.

        :param count: Number of indices to draw. Defaults to `self.index_count`.
        :param mode: OpenGL primitive type (GL_TRIANGLES, GL_LINES, etc.).
        :param dtype: Data type of indices (GL_UNSIGNED_BYTE, GL_UNSIGNED_SHORT, GL_UNSIGNED_INT).
        :param offset: Byte offset into the EBO.
        """
        if not self.ebo:
            raise RuntimeError("No element buffer (EBO) bound for draw_elements()")

        if not count:
            count = self.index_count

        # Bind buffers and set up attribute pointers
        with self:
            # Legacy client states still required
            with legacy_client_states(GL_VERTEX_ARRAY, GL_COLOR_ARRAY, GL_NORMAL_ARRAY):
                # Bind each VBO (legacy-style)
                for vbo in self.vbos.values():
                    vbo.bind()

                # Bind EBO for indexed drawing
                glBindBuffer(
                    GL_ELEMENT_ARRAY_BUFFER, getattr(self.ebo, "_id", self.ebo)
                )
                glDrawElements(mode, count, dtype, ctypes.c_void_p(offset))
                # Unbind EBO afterwards to prevent accidental reuse
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    def set_layout(self, layout: LayoutDescriptor) -> None:
        self.layout = layout

    def bind(self) -> None:
        """Bind buffers and upload attribute pointers per stored layout."""
        if not self.layout:
            return
        for attr in self.layout.attributes:
            canonical = NAME_ALIASES.get(attr.name, attr.name)
            vbo = self.vbos.get(canonical)
            if not vbo:
                continue
            glBindBuffer(GL_ARRAY_BUFFER, getattr(vbo, "_id", vbo))
            glEnableVertexAttribArray(attr.index)
            glVertexAttribPointer(
                attr.index,
                attr.size,
                attr.type,
                attr.normalized,
                attr.stride,
                ctypes.c_void_p(attr.offset),
            )

    def unbind(self) -> None:
        """Disable attribute arrays and unbind the array buffer."""
        if not self.layout:
            return
        for attr in self.layout.attributes:
            glDisableVertexAttribArray(attr.index)
        glBindBuffer(GL_ARRAY_BUFFER, 0)


