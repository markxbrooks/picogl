

import OpenGL.GLUT as GLUT
import sys
import OpenGL.GL as GL
import OpenGL.GLU as GLU


class GlutWindow(object):

    def __init__(self,*args,**kwargs):

        self.init_glut()
        self.controller = None
        self.update_if = GLUT.glutPostRedisplay

    def init_glut(self):
        GLUT.glutInit(sys.argv)
        GLUT.glutInitDisplayMode(GLUT.GLUT_RGBA | GLUT.GLUT_DOUBLE | GLUT.GLUT_DEPTH)
        GLUT.glutInitWindowSize(800, 480)
        self.window = GLUT.glutCreateWindow(b"window")
        GLUT.glutDisplayFunc(self.display)
        GLUT.glutReshapeFunc(self.resizeGL)
        GLUT.glutKeyboardFunc(self.on_keyboard)
        GLUT.glutSpecialFunc(self.on_special_key)
        GLUT.glutMouseFunc(self.on_mouse)
        GLUT.glutMotionFunc(self.on_mousemove)

    def initializeGL(self):
        GL.glClearColor(0.0, 0, 0.4, 0)
        GL.glDepthFunc(GL.GL_LESS)
        GL.glEnable(GL.GL_DEPTH_TEST)
        
    def paintGL(self):
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINES)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GLU.gluLookAt(4.0, 3.0, -3.0,
                      0.0, 0.0, 0.0,
                      0.0, 1.0, 0.0)
        #built in model
        GLUT.glutSolidTeapot(1)
        print("please override paintGL")

    def display(self):    
        self.paintGL()
        GLUT.glutSwapBuffers()

    def idle(self):
        pass

    def resizeGL(self, width, height):
        print("please overrider resize")
        self.width = width
        self.height = height
        GL.glViewport(0, 0, width, height)
        GLU.gluPerspective(45.0, float(width) / float(height), 0.1, 1000.0)

    def on_keyboard(self,key,x,y):     
        if(self.controller!=None):
              self.controller.on_keyboard(key,x,y)
        else:
            print("please overrider on_keyboard")

    def on_special_key(self,key,x,y):     
        if(self.controller!=None):
              self.controller.on_special_key(key,x,y)
        else:
            print("please overrider on_keyboard")
        
    def on_mouse(self,*args,**kwargs):
        if(self.controller!=None):
              self.controller.on_mouse(*args,**kwargs)
        else:        
            print("please overrider on_mouse")

    def on_mousemove(self,*args,**kwargs):
        if(self.controller!=None):
              self.controller.on_mousemove(*args,**kwargs)
        else:                
            print("please overrider on_mousemove")

    def run(self):
        GLUT.glutMainLoop()


if __name__ == "__main__":

    win = GlutWindow()
    win.run()