from typing import Callable

from OpenGL.raw.GL.VERSION.GL_1_0 import glClear, glClearColor, glDepthFunc, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_LESS, glEnable, GL_DEPTH_TEST, GL_CULL_FACE

from picogl.logger import Logger as log

def execute_gl_tasks(task_list: list[tuple[str, Callable]]):
    """
    Execute a sequence of OpenGL-related tasks.

    Each task is a tuple ``(message, func)``:
    - ``message`` (*str* or ``None``): If a string, it is logged before running the task.
      If ``None``, no log message is emitted for that step.
    - ``func`` (*callable*): The function to execute.

    :param task_list:
        A list of ``(message, callable)`` tuples describing the tasks to run.
    :type task_list: list[tuple[str | None, callable]]

    :raises TypeError:
        If ``task_list`` is not a list or any element is not a 2-tuple.
    :raises Exception:
        Logs and re-raises any exception thrown by a task.
    """
    if not isinstance(task_list, list):
        raise TypeError("task_list must be a list of (message, callable) tuples.")

    for i, task in enumerate(task_list, start=1):
        if not (isinstance(task, tuple) and len(task) == 2):
            log.error(f"Task #{i} is invalid. Expected tuple (str|None, callable), got {task!r}")
            continue

        message, func = task

        if message is not None and not isinstance(message, str):
            log.error(f"Task #{i} skipped: message must be str or None, got {type(message).__name__}")
            continue

        if not callable(func):
            log.error(f"Task #{i} skipped: second element must be callable, got {type(func).__name__}")
            continue

        if message:
            log.message(f"[{i}/{len(task_list)}] {message}")

        try:
            func()
        except Exception as ex:
            log.error(f"Error in task #{i} ({message or 'no message'}): {ex}", exc_info=True)
            raise


def execute_gl_tasks_old(checklist: list[tuple[str, callable]]):
    """
    Run a sequence of OpenGL initialization steps from a checklist.

    Parameters
    ----------
    checklist : list of (message, func)
        Each tuple contains:
        - message (str): A log message describing the step
        - func (callable): A callable that runs the OpenGL step
    """
    for message, func in checklist:
        log.message(message)
        func()


gl_init_list = [
    ("Initializing OpenGL context...", lambda: None),  # Message only
    ("Setting clear color", lambda: glClearColor(0.0, 0.0, 0.4, 0.0)),
    ("Setting depth function", lambda: glDepthFunc(GL_LESS)),
    ("Enabling depth test", lambda: glEnable(GL_DEPTH_TEST)),
    ("Enabling face culling", lambda: glEnable(GL_CULL_FACE)),
]

paintgl_list = [
    ("Initialising PaintGl", lambda: glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)),
]

