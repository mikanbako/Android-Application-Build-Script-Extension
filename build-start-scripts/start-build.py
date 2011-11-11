#!/usr/bin/env python
# coding: UTF-8

# Copyright 2011 Keita Kita
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Script for build.
#
# To print this usage with --help or -h option.

import argparse
import os
import os.path
import re

# Path of Ant library directory for this build scripts.
ANT_LIBRARY_DIRECTORY_PATH = os.path.join('build', 'externals', 'lib')

# Command and arguments for Ant execution.
ANT_EXEC_COMMAND = 'ant'
ANT_EXEC_ARGUMENTS = [ANT_EXEC_COMMAND, '-lib', ANT_LIBRARY_DIRECTORY_PATH,
        '-Dextended.build=true']

# Targets
TARGET_CLEAN = 'clean'
TARGET_CLEAN_ALL = 'clean-all'
TARGET_HELP = 'help'

def rewrite_targets(targets):
    ''' Rewrite element of arguments to target of build script. '''
    if TARGET_CLEAN in targets:
        targets[targets.index(TARGET_CLEAN)] = TARGET_CLEAN_ALL

def print_project_help():
    ''' Print project help. '''
    os.execvp(ANT_EXEC_COMMAND, ANT_EXEC_ARGUMENTS + ['-p'])

def run_targets(ant_properties, targets):
    ''' Run targets. '''
    os.execvp(ANT_EXEC_COMMAND, ANT_EXEC_ARGUMENTS + ant_properties + targets)

class PropertyAction(argparse.Action):
    ''' Action of ArgumentParser for Ant property. '''

    PROPERTY_PATTERN = re.compile(ur'^(?P<name>[^=]+)=(?P<value>.*)$')

    def __call__(self, parser, namespace, values, option_string):
        property_arguments = getattr(namespace, self.dest)
        if not property_arguments:
            property_arguments = []
        property_arguments.append('-D' + values[0])
        setattr(namespace, self.dest, property_arguments)

def main():
    parser = argparse.ArgumentParser(
            description='Run build.', add_help=False)
    parser.add_argument('-D', action=PropertyAction, nargs=1,
            help="Property of Ant. -D<name>=<value>.")
    parser.add_argument('--help', '-h', action='store_true',
            default=False, help='Print targets')
    parser.add_argument('target', nargs='*', help='Running targets.')

    arguments = parser.parse_args()
    rewrite_targets(arguments.target)

    if arguments.D:
        ant_properties = arguments.D
    else:
        ant_properties = []

    if arguments.help or (TARGET_HELP in arguments.target):
        print_project_help()
    elif not arguments.target:
        print_project_help()
    else:
        run_targets(ant_properties, arguments.target)

if __name__ == '__main__':
    main()
