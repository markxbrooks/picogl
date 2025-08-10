from pyglm import glm


def calculate_mvp_matrix(context: object, width: int = 1920, height: int = 1080):
    """
    calculate_mvp_matrix

    :param context: GlContext
    :param width: int
    :param height: int
    """
    context.projection = glm.perspective(glm.radians(45.0), float(width) / float(height), 0.1, 1000.0)
    context.view =  glm.lookAt(glm.vec3(4, 3, -3),  # Camera is at (4,3,-3), in World Space
                                    glm.vec3(0,0,0),  #and looks at the (0.0.0))
                                    glm.vec3(0,1,0)) #Head is up (set to 0,-1,0 to look upside-down)
    context.model = glm.mat4(1.0)
    context.mvp_matrix = context.projection * context.view * context.model
