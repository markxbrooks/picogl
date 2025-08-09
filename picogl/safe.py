"""
glGenSafe

Example Usage:
==============
>>>self.hetatm_buffers_vao = glGenSafe(glGenVertexArrays)
...self.hetatm_buffers_vbo_pos = glGenSafe(glGenBuffers)

"""

from typing import Callable, Sequence, Union


def glGenSafe(
    gen_func: Callable[[int], Union[int, list[int], tuple[int], "np.ndarray"]],
    count: int = 1,
) -> int:
    """
    glGenSafe

    :param gen_func: Callable An OpenGL generator function like glGenVertexArrays or glGenBuffers
    :param count: Number of items to generate (default is 1)
    :return: The first generated OpenGL handle (GLuint)
    Calls an OpenGL glGen* function safely and returns a single GLuint handle.
    """
    result = gen_func(count)
    if isinstance(result, (list, tuple)):
        return result[0]
    elif hasattr(result, "__getitem__") and not isinstance(result, (int, float, str)):
        try:
            return result[0]
        except Exception:
            return int(result)
    return int(result)


def glDeleteSafe(
    delete_func: Callable[[int, Union[int, Sequence[int]]], None],
    handle: Union[int, Sequence[int]],
) -> None:
    """
    glDeleteSafe

    :param delete_func: An OpenGL delete function like glDeleteBuffers or glDeleteVertexArrays
    :param handle: A single handle (int) or a sequence of handles (list/tuple/data)
    Safely deletes OpenGL resources using glDelete* functions.
    """
    if isinstance(handle, int):
        delete_func(1, [handle])
    elif isinstance(handle, (list, tuple)):
        delete_func(len(handle), handle)
    elif hasattr(handle, "__len__"):
        delete_func(len(handle), handle)
    else:
        raise TypeError(f"Invalid handle type for deletion: {type(handle)}")
