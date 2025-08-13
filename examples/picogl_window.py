from pyglm import glm
from OpenGL.raw.GL.VERSION.GL_1_0 import glViewport

from examples.utils.glutWindow import GlutWindow
from picogl.logger import setup_logging, Logger as log
from picogl.utils.gl_init import execute_gl_tasks, gl_init_list, paintgl_list


class PicoGLWindow(GlutWindow):
    """PicoGL Rendered Window"""
    def __init__(self, width, height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.renderer = None
        self.context = self.GLContext()
        self.width = width
        self.height = height
        # Mouse interaction state
        self.last_mouse_x = None
        self.last_mouse_y = None
        self.rotation_x = 0.0
        self.rotation_y = 0.0
        setup_logging()

    class GLContext(object):
        pass

    def initializeGL(self):
        """Initial OpenGL configuration."""
        log.message("Initializing OpenGL context...")
        execute_gl_tasks(gl_init_list)
        self.renderer.initialize_shaders()
        self.renderer.initialize_buffers()

    def calculate_mvp_matrix(self, width=1920, height=1080):
        """calculate_mvp_matrix"""
        self.context.projection = glm.perspective(glm.radians(45.0), float(width) / float(height), 0.1, 1000.0)
        self.context.view =  glm.lookAt(glm.vec3(4, 3, -3),  # Camera is at (4,3,-3), in World Space
                                        glm.vec3(0,0,0),  #and looks at the (0.0.0))
                                        glm.vec3(0,1,0)) #Head is up (set to 0,-1,0 to look upside-down)
        # Fixed Cube Size
        self.context.model=  glm.mat4(1.0)
        self.context.mvp_matrix = self.context.projection * self.context.view * self.context.model

    def resizeGL(self, width, height):
        """resizeGL"""
        log.message(f"Resizing viewport to {width}x{height}...")
        self.width = width
        self.height = height
        glViewport(0, 0, width, height)
        self.calculate_mvp_matrix(width, height)

    def paintGL(self):
        """paintGL"""
        print("paintgl")
        execute_gl_tasks(paintgl_list)
        self.renderer.render()

    def update_mvp_matrix(self):
        """Base perspective matrix from your existing method"""
        width, height = self.get_size()
        self.calculate_mvp_matrix(width, height)

        # Apply rotations
        rotation_matrix = glm.rotate(glm.mat4(1.0), glm.radians(self.rotation_x), glm.vec3(1, 0, 0))
        rotation_matrix = glm.rotate(rotation_matrix, glm.radians(self.rotation_y), glm.vec3(0, 1, 0))
        self.context.mvp_matrix = self.context.mvp_matrix * rotation_matrix

        self.paintGL()  # Trigger repaint

    def on_mouse(self, button, state, x, y):
        """ on mouse """
        if state == 0:  # Mouse button pressed
            self.last_mouse_x = x
            self.last_mouse_y = y

    def on_mousemove(self, x, y):
        """ on mouse move """
        if self.last_mouse_x is not None and self.last_mouse_y is not None:
            dx = x - self.last_mouse_x
            dy = y - self.last_mouse_y

            # Adjust sensitivity as needed
            self.rotation_x += dy * 0.5
            self.rotation_y += dx * 0.5

            self.update_mvp_matrix()

        self.last_mouse_x = x
        self.last_mouse_y = y

    def get_size(self):
        return self.width, self.height
