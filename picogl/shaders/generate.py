from typing import Optional

from PySide6.QtOpenGL import QOpenGLShaderProgram

from picogl.logger import Logger as log
from picogl.shaders.compile import qt_compile_shaders


def generate_shader_programs(
    vertex_shader_src: str, fragment_shader_src: str, shader_name: str = "default"
) -> Optional[QOpenGLShaderProgram]:
    """
    generate_shader_programs

    :param vertex_shader_src: str
    :param fragment_shader_src: str
    :param shader_name: str
    :return: tuple[QOpenGLShaderProgram, GluInt]
    """
    qt_shader_program = qt_compile_shaders(
        vertex_shader_src, fragment_shader_src, shader_name
    )
    if qt_shader_program is None:
        return None
    shader_program = qt_shader_program.programId()  # ✅ This is safe for glUseProgram
    if shader_program is None:
        log.error(
            "❌ Shader shader_program could not be created. Aborting scene initialization."
        )
        return None
    return qt_shader_program
