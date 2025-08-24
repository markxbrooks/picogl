from dataclasses import dataclass
from typing import List


@dataclass
class AttributeSpec:
    name: str  # semantic name ("positions", "colors", "normals", etc.)
    index: int  # attribute location
    size: int  # number of components (e.g., 3 for vec3)
    type: int  # GL_FLOAT, GL_INT, etc.
    normalized: bool
    stride: int
    offset: int  # in bytes


@dataclass
class LayoutDescriptor:
    attributes: List[AttributeSpec]
