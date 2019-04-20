import sshell
import unittest


class TestCommandMethods(unittest.TestCase):

    def test_parseCommand(self):
        self.assertEqual(sshell.parseCommand(''), [''])
        cmdIn = 'ls -l /tmp'
        self.assertEqual(sshell.parseCommand(cmdIn), ['ls', '-l', '/tmp'])

    def test_builtin_exit(self):
        with self.assertRaises(SystemExit) as exitCode:
            sshell.builtin_exit(['exit'])
        self.assertEqual(exitCode.exception.code, 0)
        with self.assertRaises(SystemExit) as exitCode:
            sshell.builtin_exit(['exit', '-1'])
        self.assertEqual(exitCode.exception.code, -1)


if __name__ == '__main__':
    unittest.main()
