#!/usr/bin/env python
# coding: UTF-8
import argparse
import os
import os.path

# Script for private build.
#
# To print this usage with --help or -h option.

# Path of Ant library directory for this build scripts.
ANT_LIBRARY_DIRECTORY_PATH = os.path.join('build', 'externals', 'lib')

# Command and arguments for Ant execution.
ANT_EXEC_COMMAND = 'ant'
ANT_EXEC_ARGUMENTS = [ANT_EXEC_COMMAND, '-lib', ANT_LIBRARY_DIRECTORY_PATH]

# Targets
TARGET_CLEAN = 'clean'
TARGET_CLEAN_ALL = 'clean-all'
TARGET_HELP = 'help'
TARGET_PRIVATE_BUILD = 'private-build'

# Default targets.
DEFAULT_TARGETS = [TARGET_PRIVATE_BUILD]

def rewrite_targets(targets):
    ''' Rewrite element of arguments to target of build script. '''
    if TARGET_CLEAN in targets:
        targets[targets.index(TARGET_CLEAN)] = TARGET_CLEAN_ALL

def print_project_help():
    ''' Print project help. '''
    os.execvp(ANT_EXEC_COMMAND, ANT_EXEC_ARGUMENTS + ['-p'])

def run_targets(targets):
    ''' Run targets. '''
    os.execvp(ANT_EXEC_COMMAND, ANT_EXEC_ARGUMENTS + targets)

def main():
    parser = argparse.ArgumentParser(
            description='Run private build.', add_help=False)
    parser.add_argument('--help', '-h', action='store_true',
            default=False, help='Print targets')
    parser.add_argument('target', nargs='*', help='Running targets.')

    arguments = parser.parse_args()
    rewrite_targets(arguments.target)

    if arguments.help or (TARGET_HELP in arguments.target):
        print_project_help()
    elif not arguments.target:
        run_targets(DEFAULT_TARGETS)
    else:
        run_targets(arguments.target)

if __name__ == '__main__':
    main()
