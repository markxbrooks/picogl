"""
Legacy Client States context manager
"""

from contextlib import contextmanager

from OpenGL.raw.GL.VERSION.GL_1_1 import (glDisableClientState,
                                          glEnableClientState)
from OpenGL.raw.GL.VERSION.GL_1_5 import GL_ARRAY_BUFFER, glBindBuffer


@contextmanager
def legacy_client_states(*states):
    """legacy client states context manager"""
    for state in states:
        glEnableClientState(state)
    try:
        yield
    finally:
        for state in reversed(states):
            glDisableClientState(state)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
