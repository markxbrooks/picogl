"""
Abstract render atoms_buffers class
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class AttributeSpec:
    index: int          # attribute location
    size: int           # number of components (e.g., 3 for vec3)
    type: int           # GL_FLOAT, GL_INT, etc.
    normalized: bool
    stride: int
    offset: int

@dataclass
class LayoutDescriptor:
    attributes: List[AttributeSpec]
    
    
Public façade
class VertexArrayGroup(ABC):
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

    @abstractmethod
    def attach_buffers(self,
                       nbo=None,
                       cbo=None,
                       vbo=None,
                       ebo=None) -> None:
        """Attach the buffers that the VAO/group should coordinate."""
        pass
        
class AbstractVertexBuffer:
    """Generic OpenGL object interface with binding lifecycle."""

    def __init__(self, handle=None):
        self.handle = handle

    def bind(self):
        raise NotImplementedError

    def unbind(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def __enter__(self):
        self.bind()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unbind()