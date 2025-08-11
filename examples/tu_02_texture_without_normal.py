# import os,sys
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import os

from OpenGL.GL import *  # pylint: disable=W0614

from pyglm import glm

from examples.data import g_vertex_buffer_data, g_uv_buffer_data
from picogl.backend.modern.core.shader.shader import PicoGLShader
from picogl.backend.modern.core.vertex.array.object import VertexArrayObject
from picogl.logger import setup_logging, Logger as log
from picogl.renderer.base import RendererBase
from picogl.utils.gl_init import init_gl_context, gl_init_list
from picogl.utils.reshape import to_float32_row
from utils.textureLoader import textureLoader
from utils.glutWindow import GlutWindow

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
GLSL_DIR = os.path.join(CURRENT_DIR, "glsl", "tu02")


class BasicObjectRenderer(RendererBase):
    """ Basic renderer class """
    def __init__(self, context):
        super().__init__()
        self.context = context
        self.show_model = True
        self.context.cube_data_positions = to_float32_row(g_vertex_buffer_data)
        self.context.vertex_count = len(self.context.cube_data_positions.flatten()) // 3

    def initialize_shaders(self):
        """Load and compile shaders."""
        log.message("Loading shaders...")
        self.context.shader = PicoGLShader(vertex_source_file="vertex.glsl",
                                   fragment_source_file="fragment.glsl",
                                   base_dir=GLSL_DIR)
        self.context.mvp_id = self.context.shader.get_uniform_location(uniform_name="mvp_matrix")
        log.parameter("MVP uniform ID: ", self.context.mvp_id)

    def initialize_rendering_buffers(self):
        """initialize buffers"""

        self.context.vertex = glGenVertexArrays(1) # pylint: disable=W0612
        glBindVertexArray(self.context.vertex)

        self.context.shader = shader = PicoGLShader(vertex_source_file="vertex.glsl",
                                   fragment_source_file="fragment.glsl",
                                   base_dir=GLSL_DIR)

        self.context.mvp_id   = shader.get_uniform_location("mvp_matrix")
        self.context.texture_id =  shader.get_uniform_location("myTextureSampler")

        texture = textureLoader("resources/tu02/uvtemplate.tga")

        self.context.textureGLID = texture.textureGLID

        self.context.vertexbuffer  = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER,self.context.vertexbuffer)
        glBufferData(GL_ARRAY_BUFFER,len(g_vertex_buffer_data)*4,(GLfloat * len(g_vertex_buffer_data))(*g_vertex_buffer_data),GL_STATIC_DRAW)

        if(texture.inversedVCoords):
            for index in range(0,len(g_uv_buffer_data)):
                if(index % 2):
                    g_uv_buffer_data[index] = 1.0 - g_uv_buffer_data[index]

        self.context.uvbuffer  = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER,self.context.uvbuffer)
        glBufferData(GL_ARRAY_BUFFER,len(g_uv_buffer_data)*4,(GLfloat * len(g_uv_buffer_data))(*g_uv_buffer_data),GL_STATIC_DRAW)

    def render(self) -> None:
        """
        render dispatcher
        :return: None
        """
        if self.show_model:
            self._draw_model()
        # Add more conditions and corresponding draw functions as needed
        self._finalize_render()

    def _draw_model(self):
        """Draw the model"""
        #print(self.context.MVP)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        cube_vao = VertexArrayObject(self.context.vertex)
        with self.context.shader, cube_vao:

            glUniformMatrix4fv(self.context.mvp_id, 1, GL_FALSE, glm.value_ptr(self.context.mvp_matrix))

            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.context.textureGLID)
            glUniform1i(self.context.texture_id, 0)

            glEnableVertexAttribArray(0)
            glBindBuffer(GL_ARRAY_BUFFER, self.context.vertexbuffer)
            glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,None)

            glEnableVertexAttribArray(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.context.uvbuffer)
            glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,0,None)


            glDrawArrays(GL_TRIANGLES, 0, 12*3) # 12*3 indices starting at 0 -> 12 triangles

            glDisableVertexAttribArray(0)
            glDisableVertexAttribArray(1)

class TextureWindow(GlutWindow):
    
    def __init__(self, width, height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = self.GLContext()
        self.renderer = BasicObjectRenderer(self.context)
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
        init_gl_context(gl_init_list)

    def calculate_mvp_matrix(self, width=1920, height=1080):
        """calculate_mvp_matrix"""
        self.context.projection = glm.perspective(glm.radians(45.0), float(width) / float(height), 0.1, 1000.0)
        self.context.view =  glm.lookAt(glm.vec3(4, 3, -3),  # Camera is at (4,3,-3), in World Space
                                        glm.vec3(0,0,0),  #and looks at the (0.0.0))
                                        glm.vec3(0,1,0)) #Head is up (set to 0,-1,0 to look upside-down)
        #fixed Cube Size
        self.context.model=  glm.mat4(1.0)
        #print(self.context.Model
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


if __name__ == "__main__":

    win = TextureWindow(width=800, height=600)
    win.initializeGL()
    win.renderer.initialize_rendering_buffers()
    win.run()
