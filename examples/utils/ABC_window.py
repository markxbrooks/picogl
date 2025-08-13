import sys
from abc import ABC, abstractmethod
from typing import Optional

# Import GLUT/OpenGL with explicit names to avoid shadowing
from OpenGL.GLUT import (
    glutInit,
    glutInitDisplayMode,
    GLUT_RGBA,
    GLUT_DOUBLE,
    GLUT_DEPTH,
    glutInitWindowSize,
    glutCreateWindow,
    glutDisplayFunc,
    glutIdleFunc,
    glutReshapeFunc,
    glutKeyboardFunc,
    glutSpecialFunc,
    glutMouseFunc,
    glutMotionFunc,
    glutSwapBuffers,
    glutMainLoop,
)
from OpenGL import GL as gl
from OpenGL.GLU import gluPerspective  # if you need it in resizeGL

class AbstractGlutWindow(ABC):
    """
    A strict ABC base class for a GLUT/OpenGL window.

    Subclasses must implement:
      - initializeGL
      - paintGL
      - resizeGL
      - on_keyboard
      - on_special_key
      - on_mouse
      - on_mousemove
    """

    def __init__(self, width: int = 800, height: int = 480, title: bytes = b"window"):
        self.controller: Optional[object] = None
        self.width = width
        self.height = height
        self.window = None

        self._init_glut(title)

    def _init_glut(self, title: bytes) -> None:
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        self.window = glutCreateWindow(title)

        # Bind GLUT callbacks to methods (which are implemented by the subclass)
        glutDisplayFunc(self.display)
        # If you want continuous redraw, uncomment:
        # glutIdleFunc(self.display)
        glutReshapeFunc(self.resizeGL)
        glutKeyboardFunc(self.on_keyboard)
        glutSpecialFunc(self.on_special_key)
        glutMouseFunc(self.on_mouse)
        glutMotionFunc(self.on_mousemove)

        self.initializeGL()

    @abstractmethod
    def initializeGL(self) -> None:
        """Set up OpenGL state. Must be implemented by subclass."""
        pass

    @abstractmethod
    def paintGL(self) -> None:
        """Render the scene. Must be implemented by subclass."""
        pass

    def display(self) -> None:
        # Default display path calls paintGL, then swaps buffers
        self.paintGL()
        glutSwapBuffers()

    def idle(self) -> None:
        """Optional idle hook (override if needed)."""
        pass

    @abstractmethod
    def resizeGL(self, width: int, height: int) -> None:
        """Handle window resize. Must be implemented by subclass."""
        pass

    @abstractmethod
    def on_keyboard(self, key, x, y) -> None:
        """Handle ASCII keyboard input. Must be implemented by subclass."""
        pass

    @abstractmethod
    def on_special_key(self, key, x, y) -> None:
        """Handle special keys (arrows, function keys). Must be implemented by subclass."""
        pass

    @abstractmethod
    def on_mouse(self, *args, **kwargs) -> None:
        """Handle mouse button events. Must be implemented by subclass."""
        pass

    @abstractmethod
    def on_mousemove(self, *args, **kwargs) -> None:
        """Handle mouse movement events. Must be implemented by subclass."""
        pass

    def run(self) -> None:
        glutMainLoop()
