from picogl.renderer import GLContext
from picogl.renderer.object import ObjectRenderer
from picogl.ui.backend.glut.renderer.glut import GlutRendererWindow


class ColoredObjectWindow(GlutRendererWindow):
    """colored with no texture"""
    def __init__(self, width, height, title,  data, glsl_dir, *args, **kwargs):
        super().__init__(width=width, height=height, title=title, *args, **kwargs)
        self.context = GLContext()
        self.data = data
        self.glsl_dir = glsl_dir
        self.renderer = ObjectRenderer(
            context=self.context,
            data=self.data,
            glsl_dir=self.glsl_dir,
        )
        self.renderer.show_model = True  # set here whether to show the cube