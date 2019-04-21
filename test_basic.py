import os
import sshell
import unittest

from unittest.mock import patch


def raise_(*args):
    raise RuntimeWarning


class TestBuildinMethods(unittest.TestCase):

    def test_buildin_exit(self):
        with self.assertRaises(SystemExit) as exitCode:
            sshell.builtin_exit(['exit'])
        self.assertEqual(exitCode.exception.code, 0)
        with self.assertRaises(SystemExit) as exitCode:
            sshell.builtin_exit(['exit', '-1'])
        self.assertEqual(exitCode.exception.code, -1)

    def test_builtin_cd(self):
        sshell.builtin_cd([''])
        self.assertEqual(os.getcwd(), '/')
        sshell.builtin_cd(['cd', '/tmp'])
        self.assertEqual(os.getcwd(), '/tmp')
        sshell.builtin_cd(['cd', '..'])
        self.assertEqual(os.getcwd(), '/')


class TestCommandMethods(unittest.TestCase):

    def test_parseCommand(self):
        self.assertEqual(sshell.parseCommand(''), [''])
        cmdIn = 'ls -l /tmp'
        self.assertEqual(sshell.parseCommand(cmdIn), ['ls', '-l', '/tmp'])

    def test_runCommand_exit(self):
        with self.assertRaises(SystemExit):
            sshell.runCommand(['exit'])

    def test_runCommand_cd(self):
        sshell.runCommand(['cd'])
        self.assertEqual(os.getcwd(), '/')

    @patch.object(os, 'fork')
    @patch.object(os, 'execvp', raise_)
    @patch.object(os, 'wait', raise_)
    def test_runCommand_command(self, mock_methods):
        os.fork.return_value = 0  # Child Branch
        with self.assertRaises(RuntimeWarning):
            sshell.runCommand(['bash'])
        os.fork.return_value = 1  # parent Branch
        with self.assertRaises(RuntimeWarning):
            sshell.runCommand(['bash'])


if __name__ == '__main__':
    unittest.main()
