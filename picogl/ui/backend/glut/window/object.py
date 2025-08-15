from picogl.renderer import GLContext, MeshData
from picogl.renderer.object import ObjectRenderer
from picogl.ui.backend.glut.window.glut_renderer import GlutRendererWindow
from picogl.utils.loader.object import OBJLoader


class ObjectWindow(GlutRendererWindow):
    """ Object Window"""
    def __init__(self, width, height, title, object_file_name, glsl_dir, *args, **kwargs):
        super().__init__(width, height, title, *args, **kwargs)
        self.glsl_dir = glsl_dir
        self.context = GLContext()
        obj_loader = OBJLoader(object_file_name)
        self.data = obj_loader.to_array_style()

        self.renderer = ObjectRenderer(
            context=self.context,
            data=MeshData.from_raw(
                vertices=self.data.vertices,
                normals=self.data.normals,
                colors=([[1.0, 0.0, 0.0]] * (len(self.data.vertices)//3))
            ),
            glsl_dir=self.glsl_dir,
        )