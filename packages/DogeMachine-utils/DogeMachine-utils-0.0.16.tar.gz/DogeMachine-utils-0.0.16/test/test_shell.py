import os
import unittest
import json
import logging
import subprocess
import warnings
from dogemachine_utils.shell import run_shell_command
from dogemachine_utils.testing_utils import ignore_warnings
from dogemachine_utils.log_formatting import set_stream_logger
logger = logging.getLogger(__name__)
warnings.simplefilter("ignore", ResourceWarning)


class ShellTestCase(unittest.TestCase):

    def test_run_shell_command_wait(self):
        command = "echo 'sup'"
        results = run_shell_command(command=command, timeout=5, shell=False)
        print(results.__dict__)
        self.assertTrue(results.stdout == "sup\n")
        self.assertTrue(results.returncode == 0)

    @ignore_warnings
    def test_run_shell_command_dont_wait(self):
        command = "echo 'sup'"
        # unittest.main(warnings='ignore')
        results = run_shell_command(command=command, timeout=5, shell=False, wait_for_finish=False)
        print(results.__dict__)
        print(results.stdout.__dict__)
