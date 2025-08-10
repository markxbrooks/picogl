# import os,sys
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import os

from OpenGL.GL import *  # pylint: disable=W0614

from pyglm import glm

from picogl.backend.modern.core.shader.shader import PicoGLShader
from utils.glutWindow import GlutWindow

from picogl.logger import setup_logging, Logger as log
from examples.data import g_vertex_buffer_data, g_color_buffer_data

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

setup_logging()


class Tu01Win(GlutWindow):

	class GLContext(object):
		pass
	def init_opengl(self):
		glClearColor(0.0,0,0.4,0)
		glDepthFunc(GL_LESS)
		glEnable(GL_DEPTH_TEST)
		glEnable(GL_CULL_FACE)

	def initialize_buffers(self):
		"""
		initialize_buffers
		"""
		self.context = self.GLContext()
		self.shader = shader = PicoGLShader()
		shader.init_shader_from_glsl_files("glsl/tu01/vertex.glsl",
										   "glsl/tu01/fragment.glsl",
										   base_dir=CURRENT_DIR)
		self.context.mvp_id = self.get_uniform_location(shader=shader,
														uniform_name="mvp_matrix")
		self.context.vertex_buffer = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.context.vertex_buffer)
		glBufferData(GL_ARRAY_BUFFER, len(g_vertex_buffer_data) * 4, (GLfloat * len(
			g_vertex_buffer_data))(*g_vertex_buffer_data), GL_STATIC_DRAW)
		self.context.color_buffer  = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.context.color_buffer)
		glBufferData(GL_ARRAY_BUFFER, len(g_color_buffer_data) * 4, (GLfloat * len(
			g_color_buffer_data))(*g_color_buffer_data), GL_STATIC_DRAW)

	def get_uniform_location(self, shader, uniform_name):
		mvp_id = glGetUniformLocation(shader.program, uniform_name)
		return mvp_id

	def calculate_mvp_matrix(self, width=1920, height=1080):

		self.context.projection = glm.perspective(glm.radians(45.0), float(width) / float(height), 0.1, 1000.0)
		self.context.view =  glm.lookAt(glm.vec3(4, 3, -3),  # Camera is at (4,3,-3), in World Space
										glm.vec3(0,0,0),  #and looks at the (0.0.0))
										glm.vec3(0,1,0)) #Head is up (set to 0,-1,0 to look upside-down)

		self.context.model=  glm.mat4(1.0)

		self.context.mvp_matrix = self.context.projection * self.context.view * self.context.model

	def resize(self, width, height):

		glViewport(0, 0, width, height)
		self.calculate_mvp_matrix(width, height)

	def ogl_draw(self):

		print("draw++")
		#print self.context.mvp_matrix
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		self.shader.begin()
		glUniformMatrix4fv(self.context.mvp_id,1,GL_FALSE,glm.value_ptr(self.context.mvp_matrix))

		glEnableVertexAttribArray(0)
		glBindBuffer(GL_ARRAY_BUFFER, self.context.vertex_buffer)
		glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,None)

		glEnableVertexAttribArray(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.context.color_buffer)
		glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,0,None)


		glDrawArrays(GL_TRIANGLES, 0, 12*3) # 12*3 indices starting at 0 -> 12 triangles

		glDisableVertexAttribArray(0)
		glDisableVertexAttribArray(1)
		self.shader.end()
        

if __name__ == "__main__":

    win = Tu01Win()
    win.init_opengl()
    win.initialize_buffers()
    win.run()
