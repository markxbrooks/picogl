from OpenGL.raw.GL.VERSION.GL_1_0 import GL_RENDERER, GL_VENDOR, GL_VERSION
from OpenGL.raw.GL.VERSION.GL_2_0 import GL_SHADING_LANGUAGE_VERSION

from OpenGL.GL import glGetString


def get_gl_info():
    """Get picogl info"""
    info = """
        Vendor: {0}
        RendererBase: {1}
        OpenGL Version: {2}
        Shader Version: {3}
        """.format(
        glGetString(GL_VENDOR),
        glGetString(GL_RENDERER),
        glGetString(GL_VERSION),
        glGetString(GL_SHADING_LANGUAGE_VERSION),
    )
    return info
