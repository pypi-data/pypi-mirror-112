from contextlib import contextmanager
import logging

import rich
from rich import print as rich_print
from rich.logging import RichHandler
from rich.progress import Progress as RichProgress, BarColumn


def _configure_logging():
    console_handler = RichHandler(show_time=False, show_path=False, show_level=False)
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s,%(msecs)03d [%(name)s]: %(message)s', '%H:%M:%S')
    console_handler.setFormatter(formatter)
    dulcinea_logger = logging.getLogger("dulcinea")
    dulcinea_logger.addHandler(console_handler)
    dulcinea_logger.setLevel(logging.DEBUG)
    panza_logger = logging.getLogger("panza")
    panza_logger.addHandler(console_handler)
    panza_logger.setLevel(logging.DEBUG)
    return dulcinea_logger


class Progress:
    def __init__(self, progress, task):
        self.progress = progress
        self.task = task

    def advance(self):
        self.progress.advance(self.task)


class Output:
    def __init__(self):
        self.logger = _configure_logging()

    @contextmanager
    def progress(self, total: int):
        progress = RichProgress(
            BarColumn(bar_width=rich.get_console().size.width),
            "[[progress.percentage]{task.percentage:>3.0f}%[/]]",
            transient=True
        )
        task = progress.add_task("Progress", total=total)
        try:
            progress.start()
            yield Progress(progress, task)
        finally:
            progress.stop()

    @staticmethod
    def horizontal_rule(message: str):
        rich.get_console().rule(message, align="left")

    @staticmethod
    def print(*args, raw: bool = False):
        if not raw:
            rich_print(*args)
        else:
            print(*args)
