import subprocess  # nosec - skip B404:blacklist
import logging
import shlex
import os
import warnings
from typing import Union
logger = logging.getLogger(__name__)


def run_shell_command(
        command: str,
        shell: bool = True,
        wait_for_finish: bool = True,
        env_vars: dict = None,
        timeout: int = None
) -> Union[subprocess.Popen, subprocess.CompletedProcess]:
    """
    wrapper for subprocess.Popen.
    Given a string of a bash command, run the shell command here.
    This is risky AF, so make sure you are careful and don't use this to accept user input.
    """
    args = shlex.split(command)
    logger.debug(f"args: {args}")
    env = {
        **os.environ,
        # "TEST_VARIABLE": str(1234),
    }
    if env_vars:
        env.update(env_vars)
    # https://docs.python.org/3/library/subprocess.html#popen-constructor
    if wait_for_finish:
        process = subprocess.run(
            args=args,
            shell=shell,  # nosec - skip B404:blacklist, B603:subprocess_without_shell_equals_true
            timeout=timeout,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
            universal_newlines=True,
            env=env
        )
    else:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=ResourceWarning)
            process = subprocess.Popen(
                args=args,
                shell=shell,  # nosec - skip B404:blacklist, B603:subprocess_without_shell_equals_true
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                encoding="ascii",
                universal_newlines=True,
                env=env
            )
    logger.debug(f"{command} response: {process.stdout}")
    return process
