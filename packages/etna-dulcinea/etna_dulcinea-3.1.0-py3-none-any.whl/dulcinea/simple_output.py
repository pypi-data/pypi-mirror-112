from contextlib import contextmanager
import logging
import re


def _configure_logging():
    console_handler = logging.StreamHandler()
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
    def advance(self):
        pass


def _remove_markup(s: str) -> str:
    return re.sub(r"\[.*?]", "", s)


class Output:
    def __init__(self):
        self.logger = _configure_logging()

    @contextmanager
    def progress(self, total: int):
        yield Progress()

    def horizontal_rule(self, message: str):
        message = _remove_markup(message)
        self.logger.info(message)

    @staticmethod
    def print(*args, raw: bool = False):
        if not raw:
            args = (_remove_markup(str(arg)) for arg in args)
        print(*args)
