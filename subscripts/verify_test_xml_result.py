#!/usr/bin/env python
# coding: UTF-8

# Copyright 2012 Keita Kita
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

# Check JUnit XML whether the test is successful.
#
# This script can be ran by Jython.

# Usage :
#
#    ./check_test_xml_result.py <JUnit XML file>
#
#    If the test is successful, this script returns 0.
#    If the test is failure, this script returns 1.
#    If you give the file which is not JUnit XML, this script does not
#    guarantee the result.

import sys
import os
import xml.parsers.expat
from optparse import OptionParser

def is_test_successful(path):
    u'''
    Check whether the test is successful.

    Parameters :
        path : Path of JUnit XML result.
    Returns :
        True if the test is successful, otherwise false.
    Exceptions :
        xml.parsers.expat.ExpatError : XML parsing is failure.
        IOError : The file cannot be read.
    '''

    # Open JUnit XML file.
    junit_xml_file = open(path, 'Ur')

    # Parse JUnit XML.
    #
    # If the errors or failures attribute of testsuite element has number of
    # more than 1, the test is failure.

    parser = xml.parsers.expat.ParserCreate()

    class TestResult:
        u'''
        This class represents the result of a test.
        '''
        def __init__(self):
            self.is_successful = True

        def start_element(self, name, attributes):
            u'''
            Call when an element is started.
            '''
            if name == 'testsuite' and (
                    0 < int(attributes['errors']) or
                    0 < int(attributes['failures'])):
                self.is_successful = False

    test_result = TestResult()

    parser.StartElementHandler = test_result.start_element
    parser.ParseFile(junit_xml_file)

    return test_result.is_successful

def main():
    # Parse command line arguments.

    parser = OptionParser(usage=u'usage: %prog <JUnit XML file path>')
    (options, args) = parser.parse_args()

    # If there are not arguments, the arguments is invalid.
    if not args:
        parser.print_help()
        sys.exit(1)

    # args[0] : JUnit XML file path.
    raw_path = args[0]
    if os.path.exists(raw_path):
        junit_xml_file_path = os.path.abspath(raw_path)
    else:
        print >>sys.stderr, u'%s is not fould.' % (raw_path)
        parser.print_help()
        sys.exit(1)

    # If the test is failure, return 1.
    try:
        if is_test_successful(junit_xml_file_path):
            sys.exit()
        else:
            # sys.exit([arg]) on Jython 2.5.0 attached to Android SDK ignores
            # string type argument.
            print >>sys.stderr, u"Test is failure."
            sys.exit(1)
    except IOError, e:
        sys.exit(e.message)
    except xml.parsers.expat.ExpatError, e:
        sys.exit(u'Parsing failed. ' +
                unicode(xml.parsers.expat.ErrorString(e.code)) +
                u' at %d, %d' % (e.lineno, e.offset))

if __name__ == '__main__':
    main()
