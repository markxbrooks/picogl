from OpenGL.GLUT import GLUT as GLUT
import sys
from OpenGL import GL as gl
from OpenGL.GLU import gluLookAt, gluPerspective  # optional, for readability

from typing import Optional

class GlutWindow(object):
    def __init__(self, *args, **kwargs):
        self.controller: Optional[object] = None
        self.width = 800
        self.height = 480
        self.window = None

        # Defer comments to a dedicated init method
        self._init_glut()

    def _init_glut(self) -> None:
        """Initialize GLUT and create a window. Subclasses can override to customize."""
        GLUT.glutInit(sys.argv)
        GLUT.glutInitDisplayMode(GLUT.GLUT_RGBA | GLUT.GLUT_DOUBLE | GLUT.GLUT_DEPTH)
        GLUT.glutInitWindowSize(self.width, self.height)
        self.window = GLUT.glutCreateWindow(b"window")

        GLUT.glutDisplayFunc(self.display)
        # GLUT.glutIdleFunc(self.display)  # uncomment if you want continuous redraw
        GLUT.glutReshapeFunc(self.resizeGL)
        GLUT.glutKeyboardFunc(self.on_keyboard)
        GLUT.glutSpecialFunc(self.on_special_key)
        GLUT.glutMouseFunc(self.on_mouse)
        GLUT.glutMotionFunc(self.on_mousemove)

        self.initializeGL()

        # default update handler
        self.update_if = GLUT.glutPostRedisplay

    # Lifecycle hooks intended to be overridden
    def initializeGL(self) -> None:
        gl.glClearColor(0.0, 0.0, 0.4, 0.0)
        gl.glDepthFunc(gl.GL_LESS)
        gl.glEnable(gl.GL_DEPTH_TEST)

    def paintGL(self) -> None:
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # example usage; keep as-is for compatibility
        GLUT.glutPostRedisplay  # no-op, just to keep import side effects visible

        # If you have a teapot or other scene, keep it here
        oglut.glutSolidTeapot(1)  # adjust if you’re using teapots

        print("please override paintGL")

    def display(self) -> None:
        self.paintGL()
        GLUT.glutSwapBuffers()

    def idle(self) -> None:
        pass

    def resizeGL(self, width: int, height: int) -> None:
        print("please override resize")
        self.width = width
        self.height = height
        gl.glViewport(0, 0, width, height)
        gluPerspective(45.0, float(width) / float(height), 0.1, 1000.0)

    # Input callbacks (safely handle missing controller)
    def on_keyboard(self, key, x, y) -> None:
        if self.controller is not None:
            self.controller.on_keyboard(key, x, y)
        else:
            print("please override on_keyboard")

    def on_special_key(self, key, x, y) -> None:
        if self.controller is not None:
            self.controller.on_special_key(key, x, y)
        else:
            print("please override on_special_key")

    def on_mouse(self, *args, **kwargs) -> None:
        if self.controller is not None:
            self.controller.on_mouse(*args, **kwargs)
        else:
            print("please override on_mouse")

    def on_mousemove(self, *args, **kwargs) -> None:
        if self.controller is not None:
            self.controller.on_mousemove(*args, **kwargs)
        else:
            print("please override on_mousemove")

    def __str__(self) -> str:
        return f"GlutWindow(width={self.width}, height={self.height}, window={self.window})"

    def run(self) -> None:
        GLUT.glutMainLoop()


if __name__ == "__main__":

    win = GlutWindow()
    win.run()
