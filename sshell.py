#!/usr/bin/env python3
import sys
import os


def builtin_exit(cmd):
    if len(cmd) == 1:
        cmd.append('0')
    sys.exit(int(cmd[1]))


def builtin_cd(cmd):
    if len(cmd) == 1:
        cmd.append('/')
    os.chdir(cmd[1])


def parseCommand(cmd):
    return cmd.split(' ')


def runCommand(cmd):
    """Executes the desired command, checking for builtins"""
    if(cmd[0] == 'exit'):
        builtin_exit(cmd)
    if(cmd[0] == 'cd'):
        builtin_cd(cmd)
        return
    child = os.fork()
    if child == 0:
        os.execvp(cmd[0], cmd)
    else:
        os.wait()


if __name__ == '__main__':
    promptBegin = os.path.splitext(sys.argv[0])[0]
    while True:
        try:
            print(promptBegin, end="> ")
            command = parseCommand(input())
            if command[0] != '':
                runCommand(command)
        except EOFError as err:
            print()
            exit(0)
        except KeyboardInterrupt as err:
            print()
