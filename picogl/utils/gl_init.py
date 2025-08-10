from OpenGL.raw.GL.VERSION.GL_1_0 import glClearColor, glDepthFunc, GL_LESS, glEnable, GL_DEPTH_TEST, GL_CULL_FACE

from picogl.logger import Logger as log


def init_gl_context(checklist: list[tuple[str, callable]]):
    """
    Run a sequence of OpenGL initialization steps from a checklist.

    Parameters
    ----------
    checklist : list of (message, func)
        Each tuple contains:
        - message (str): A log message describing the step
        - func (callable): A callable that runs the OpenGL step
    """
    for message, func in checklist:
        log.message(message)
        func()


gl_init_list = [
    ("Initializing OpenGL context...", lambda: None),  # Message only
    ("Setting clear color", lambda: glClearColor(0.0, 0.0, 0.4, 0.0)),
    ("Setting depth function", lambda: glDepthFunc(GL_LESS)),
    ("Enabling depth test", lambda: glEnable(GL_DEPTH_TEST)),
    ("Enabling face culling", lambda: glEnable(GL_CULL_FACE)),
]