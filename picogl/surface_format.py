"""
Qt OpenGL Surface Format Configuration
======================================

This module configures the default OpenGL surface format
for a Qt application using PySide6.

It defines the `set_opengl_surface_format()` function,
which sets up an OpenGL 3.0 Core Profile
context with common settings including double buffering,
depth and stencil atoms_buffers, and 4x MSAA
(multisample anti-aliasing).

Functions
---------

- ``set_opengl_surface_format``:
    Applies the desired OpenGL context version, profile,
    and framebuffer attributes globally
    for all Qt OpenGL widgets.

Usage
-----

This function should be called early in the application lifecycle,
typically before creating
any `QApplication` or `QOpenGLWidget` instances,
to ensure consistent OpenGL context creation.

Requirements
------------

- PySide6.QtGui.QSurfaceFormat
- PySide6.QtOpenGL.QOpenGLVersionProfile

Note
----

This configuration assumes a **Core Profile OpenGL 3.0** context.
If legacy (Compatibility Profile)
behavior is needed, modify the `setProfile()`
call accordingly, e.g to version 3.3.

"""

from PySide6.QtGui import QSurfaceFormat


def set_opengl_surface_format():
    """
    Configure the OpenGL context format for the Qt application.
    """
    fmt = QSurfaceFormat()
    fmt.setVersion(3, 0)
    fmt.setProfile(QSurfaceFormat.CoreProfile)
    fmt.setDepthBufferSize(24)
    fmt.setStencilBufferSize(8)
    fmt.setSwapBehavior(QSurfaceFormat.DoubleBuffer)
    fmt.setRenderableType(QSurfaceFormat.OpenGL)
    fmt.setSamples(4)
