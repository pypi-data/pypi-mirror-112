import os
import logging
logger = logging.getLogger(__name__)


def write_file(file: str, content: str) -> None:
    if os.path.exists(file):
        logger.debug("%s exists. Removing the file and replacing its contents." % file)
        os.remove(file)
    with open(file, "w") as f:
        f.write(content)


def read_file(file: str) -> str:
    with open(file, "r") as f:
        content = f.read()
    return content


def create_folder(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)
