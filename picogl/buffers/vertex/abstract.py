"""
AbstractVertexGroup

Example usage
=============
>>># During setup
...atom_group = AtomBufferGroup(...)
...
...atom_group.nbo = LegacyNormalVBO(...) or ModernNormalVBO(...)
...atom_group.cbo = LegacyColorVBO(...) or ModernColorVBO(...)
...atom_group.vbo = LegacyAtomVBO(...) or ModernAtomVBO(...)
...atom_group.ebo = LegacyBondEBO(...) or ModernBondEBO(...)
...
...# Bind for rendering
...atom_group.bind()  # uses VAO path if available, or legacy re-bind path
...# draw call, e.g. glDrawElements(...) or glDrawArrays(...)

#6) Migration notes

#Public surface: keep AbstractVertexGroup as the canonical concept and hide the backend behind it.
If you had a public class named BufferGroup, consider renaming to
 AbstractVertexGroup or VertexArrayState to reflect its intent.
#Backends: keep two concrete implementations: VertexArrayGroup and ModernVertexArrayGroup.
You can expose lightweight aliases during transition
(VertexArrayGroup = LegacyVertexArrayGroupImpl, etc.) if you need to preserve import paths.
#Typing: if you want to be explicit, you can type vaog: Optional[AbstractVertexGroup]
 AtomBufferGroup and keep buffers as the specific legacy/modern types;
  move all buffers under the VAO façade entirely (the latter simplifies binding logic).

"""

from abc import ABC, abstractmethod

from picogl.buffers.attributes import LayoutDescriptor


class VertexArrayGroup(ABC):
    """Public façade"""

    @abstractmethod
    def bind(self) -> None:
        """Bind the underlying VAO/state for rendering."""
        pass

    @abstractmethod
    def unbind(self) -> None:
        """Optionally unbind the VAO/state."""
        pass

    @abstractmethod
    def delete(self) -> None:
        """Release resources (VAO or equivalent)."""
        pass

    @abstractmethod
    def set_layout(self, layout: LayoutDescriptor) -> None:
        """Define the attribute layout for this VAO/group."""
        pass

    """@abstractmethod
    def attach_buffers(self,
                       nbo=None,
                       cbo=None,
                       vbo=None,
                       ebo=None) -> None:
        ""Attach the buffers that the VAO/group should coordinate.""
        pass"""

    # Context manager support
    def __enter__(self):
        self.bind()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unbind()
