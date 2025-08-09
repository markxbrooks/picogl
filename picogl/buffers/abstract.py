"""
Abstract render atoms_buffers class
"""

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