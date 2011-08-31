#!/usr/bin/env python
# coding: UTF-8
import argparse
import sys
import re

# Validate test result represented as text.
#
# If the test failed, this script returns code -1.
# If the test succeeded, this script returns code 0.


TARGET_RUN_TESTS = 'run-tests'

# Pattern representing target starting in result.
PATTERN_TARGET_STARTED = re.compile(ur'^(?P<target>[^:]+):$')

# Pattern representing test succeeded.
PATTERN_RESULT_OK = re.compile(ur'^\s+\[exec\]\s+OK\s+\(\s*\d+\s+tests?\)$')

def extract_target_result(target, lines):
    ''' Extract target result.

        Parameters :
            target : Extracted target.
            lines : List of line.
        Return :
            Extracted list. If target is not contained, return empty list.
    '''
    target_pattern = target + ':'
    start_index = -1
    end_index = len(lines)
    current_index = 0
    for l in lines:
        match = PATTERN_TARGET_STARTED.match(l)
        if match:
            if match.group('target') == target:
                start_index = current_index
            elif 0 <= start_index:
                end_index = current_index
        current_index += 1

    if 0 <= start_index:
        return lines[start_index:end_index]
    else:
        return []

def is_succeeded(lines):
    ''' Check whether the test succeeded.

        Parameters :
            lines : List of line.
        Return :
            True if the test succeeded, false otherwise.
    '''
    for l in lines:
        if PATTERN_RESULT_OK.match(l):
            return True
    else:
        return False

def validate_test_text_result(file):
    ''' Validate test result represented as text.

        Parameters :
            file : Path of test result.
        Return :
            0 if the test succeeded. -1 if the test failed.
    '''
    with open(file, 'rU') as f:
        lines = f.readlines()

    return is_succeeded(extract_target_result(TARGET_RUN_TESTS, lines))

def main():
    parser = argparse.ArgumentParser(
            description='Validate test result represented as text.')
    parser.add_argument('test_result_file', nargs=1)

    arguments = parser.parse_args()

    if validate_test_text_result(arguments.test_result_file[0]):
        return_code = 0
    else:
        return_code = 1

    sys.exit(return_code)

if __name__ == '__main__':
    main()
