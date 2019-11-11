import os
import sshell
import unittest

from unittest.mock import patch


def raise_(*args):
    raise RuntimeWarning


class TestBuiltinMethods(unittest.TestCase):

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

    def test_parseCommand_pipe(self):
            self.assertEqual(
                sshell.parseCommand('ls -d . | wc -l'),
                [['ls', '-d', '.'], ['wc', '-l']]
                )

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

    @patch.object(os, 'fork')
    @patch.object(os, 'execvp', raise_)
    @patch.object(os, 'wait', raise_)
    def test_runCommand_badcommand(self, mock_methods):
        os.fork.return_value = 0  # Child Branch
        with self.assertRaises(RuntimeWarning):
            sshell.runCommand(['foo'])
        os.fork.return_value = 1  # parent Branch
        with self.assertRaises(RuntimeWarning):
            sshell.runCommand(['foo'])

    def test_valid_exe(self):
        from string import ascii_lowercase
        validcmd = ['/usr/bin/env']
        self.assertTrue(sshell.valid_exe(validcmd))

        # invalid command with no path
        invalidcmd = [ascii_lowercase]
        self.assertFalse(sshell.valid_exe(invalidcmd))

        # invalid command with path
        invalidcmd = ['/bin/' + ascii_lowercase]
        self.assertFalse(sshell.valid_exe(invalidcmd))


if __name__ == '__main__':
    unittest.main()
