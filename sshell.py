#!/usr/bin/env python3
import sys
import os


def valid_exe(cmd):
    def exe_check(exePath):
        return os.path.exists(exePath) and os.access(exePath, os.X_OK)

    exePath, exeName = os.path.split(cmd[0])
    if exePath:
        if exe_check(cmd[0]):
            return cmd[0]
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            exeFull = os.path.join(path, cmd[0])
            if exe_check(exeFull):
                return exe_check(cmd[0])


def builtin_exit(cmd):
    if len(cmd) == 1:
        cmd.append('0')
    sys.exit(int(cmd[1]))


def builtin_cd(cmd):
    if len(cmd) == 1:
        cmd.append('/')
    os.chdir(cmd[1])


def builtin_command(cmd):
    '''check if command is a valid executable'''
    if len(cmd) == 1:
        return
    result = valid_exe(cmd[1:])
    if result is not None:
        print(result)


def parseCommand(cmd):
    """Parses given input. checks for pipes to approrpiately nest commands"""
    if '|' in cmd:
        return [c.strip().split(' ') for c in cmd.split('|')]
    return cmd.split(' ')


def runCommand_io(cmdList):
    """Executes multiple commands, using a pipe"""
    if os.fork() == 0:
        r, w = os.pipe()
        if os.fork() == 0:
            # child child commandb
            os.dup2(r, sys.stdin.fileno())
            os.close(r)
            os.close(w)
            os.execvp(cmdList[1][0], cmdList[1])
        else:
            # child parent commanda
            os.close(r)
            os.dup2(w, sys.stdout.fileno())
            os.execvp(cmdList[0][0], cmdList[0])
            os.close(w)
    else:
        os.wait()


def runCommand(cmd):
    """Executes the desired command, checking for builtins"""
    if(type(cmd[0]) == list):
        runCommand_io(cmd)
        return
    if(cmd[0] == 'exit'):
        builtin_exit(cmd)
    if(cmd[0] == 'cd'):
        builtin_cd(cmd)
        return
    if(cmd[0] == 'command'):
        builtin_command(cmd)
        return
    try:
        child = os.fork()
        if child == 0:
            os.execvp(cmd[0], cmd)
        else:
            os.wait()
    except FileNotFoundError as err:
        print("\'%s\' command not found" % cmd[0], file=sys.stderr)
        exit(1)


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
