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
    # if os.fork() == 0:
    #    # Child
    #    os.dup2(r, sys.stdin.fileno())
    #    os.close(r)
    #    os.close(w)
    #    os.execvp(cmdList[1][0], cmdList[1])
    # else:
    #    # Parent
    #    os.close(r)
    #    os.dup2(w, sys.stdout.fileno())
    #    os.execvp(cmdList[0][0], cmdList[0])
    #    os.close(w)
    #    os.wait()


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
