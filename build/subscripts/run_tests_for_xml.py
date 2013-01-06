#!/usr/bin/env jython
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

# Run tests and output result as XML.
#
# This script must be ran by Jython. CLASSPATH environment variable must
# contain ddmlib.jar provided by Android SDK.
#
# Android emulator must launched or device must be connected.

# Usage :
#
#   1. Set path of ddmlib.jar to CLASSPATH environment variable. For example :
#
#     export CLASSPATH=<ANDROID_SDK_HOME>/tools/lib/ddmlib.jar
#
#   2. Install application and test application to your device or emulator.
#
#   3. Run this script by Jython.
#
#     Run default test runner (android.test.InstrumentationTestRunner) :
#       ./run_tests_for_xml.py -a <path_of_adb> <test_project_package_name>
#
#     Run specific test runner :
#       ./run_tests_for_xml.py -a <path_of_adb> <test_project_package_name> <test_runner_name>
#
#     Run test runner on specific device or emulator, if -s option is used.
#       ./run_tests_for_xml.py -a <path_of_adb> -s <serial_of_device> <test_project_package_name> <test_runner_name>
#
#     XML of test result is printed to standard output.
#
#     Run for detail :
#       ./run_tests_for_xml.py --help

from datetime import datetime
from datetime import timedelta
from optparse import OptionParser
from StringIO import StringIO
from threading import Event
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

import codecs
import re
import sys

from com.android.ddmlib import AndroidDebugBridge
from com.android.ddmlib.testrunner import RemoteAndroidTestRunner
from com.android.ddmlib.testrunner import ITestRunListener
from tempfile import TemporaryFile

# Pattern that represents option of serial number of device.
PATTERN_SERIAL_NUMBER_OPTION = re.compile(ur'-s\s+(?P<serial_number>[^-]\S+)')

# Encoding of outputted XML.
XML_ENCODING = u'UTF-8'

# Pattern that represents position of inserting new line of outputted XML.
PATTERN_XML_INSERTING_NEW_LINE = re.compile(ur'(?<=>)<(?=[^?/])')

# Replacement to insert new line for outputted XML.
REPLACEMENT_XML_INSERTING_NEW_LINE = u'\n\g<0>'

def get_serial_number(adb_device_arg):
    u'''
    Get serial number from adb.device.arg.

    Parameters:
        adb_device_arg : Arguments for adb.
    Return:
        Serial number. None if adb.device.arg does not contain serial number.
    '''
    match = PATTERN_SERIAL_NUMBER_OPTION.search(adb_device_arg)
    if match:
        return match.group(u'serial_number')
    else:
        return None

def get_device(serial_number, debug_bridge):
    u'''
    Get target device.

    Parameters:
        serial_number : Serial number of device or emulator. None is OK.
        debug_bridge : An instance of debug_bridge.
    Return:
        An instance of com.android.ddmlib.IDevice. None if the debug bridge
        does not connect to any devices.
    '''
    # Get connecting devices.
    devices = debug_bridge.getDevices()

    # If devices are not found.
    if not devices:
        return None

    # Select one from devices.
    if serial_number:
        # If serial number is specified, find its device.
        for d in devices:
            if d.getSerialNumber() == serial_number:
                return d
        else:
            # A device of the serial number is not found.
            return None
    else:
        # Otherwise the default device is selected.
        return devices[0]

class TestResultXmlFormatter(ITestRunListener):
    u'''
    Formatter that formats test results to XML.
    '''

    # Key of property that represents name of host.
    PROPERTY_KEY_HOST_NAME = u'net.hostname'

    # Pattern of trace of first line.
    PATTERN_TRACE_FIRST_LINE = re.compile(ur'\A(?P<type>[^:]+)(?::\s*(?P<message>.*))?\Z')

    def __init__(self, device_properties):
        u'''
        Initialize this object.

        Parameters :
            device_properties : Properties of the device.
        '''
        # Create a tree.
        self.__tree = ElementTree(Element(u'testsuite'))
        self.__test_suite_element = self.__tree.getroot()

        # Create a properties element.
        self.__device_properties = device_properties
        self.create_properties_element()

    def create_properties_element(self):
        u'''
        Create a properties element.
        '''
        # Create a properties element.
        properties = SubElement(self.__test_suite_element, u'properties')

        # Create a property elements.
        for entry in self.__device_properties.entrySet():
            SubElement(properties, u'property', {entry.key: entry.value})

    def testRunStarted(self, runName, testCount):
        # Set attributes of the testsuite element.

        self.__test_suite_element.attrib.update({
            u'name': runName,
            u'hostname':
                self.__device_properties[self.PROPERTY_KEY_HOST_NAME],
            u'tests': unicode(testCount),
            u'timestamp': unicode(datetime.now().isoformat()),
            })

        # Initialize counters.
        self.__failed_test_count = 0
        self.__error_test_count = 0

    def testStarted(self, test):
        # Create a testcase element.
        self.__current_testcase_element = SubElement(
            self.__test_suite_element, u'testcase',
            {u'classname': test.getClassName(), u'name': test.getTestName()});

        # Record the test started time.
        self.__current_test_started_time = datetime.now()

    def testFailed(self, status, test, trace):
        # Judge the kind of this failure.
        if status == ITestRunListener.TestFailure.FAILURE:
            tag = u'failure'
            self.__failed_test_count += 1
        else:
            tag = u'error'
            self.__error_test_count += 1

        # Create a failure or a error element.

        failed_element = SubElement(self.__current_testcase_element, tag)

        # Parse the error type and message.
        match = self.PATTERN_TRACE_FIRST_LINE.match(trace.splitlines(False)[0])
        if match:
            failed_element.attrib[u'type'] = match.group(u'type')
            message = match.group(u'message')
            if message:
                failed_element.attrib[u'message'] = message

        failed_element.text = trace

    def testEnded(self, test, testMetrics):
        # Record the elapsed time.
        elapsed_time = datetime.now() - self.__current_test_started_time

        # Set the time attribute to the elapsed time.
        self.__current_testcase_element.set(u'time',
            u'%d.%d' % (elapsed_time.days * 60 * 60 + elapsed_time.seconds,
                elapsed_time.microseconds))

    def testRunFailed(self, errorMessage):
        # Create a system-error element.
        system_err_element = SubElement(self.__test_suite_element, u'system-err')
        system_err_element.text = errorMessage

    def testRunEnded(self, elapsedTime, testMetrics):
        # Set attributes of the testsute.
        self.__test_suite_element.attrib.update({
            u'time': unicode(float(elapsedTime) / 1000),
            u'errors': unicode(self.__error_test_count),
            u'failures': unicode(self.__failed_test_count),
            })

    def get_result(self):
        u'''
        Get result as ElementTree.

        Return:
            ElementTree that represents result of test.
        '''
        return self.__tree

class DeviceConnectingEvent(AndroidDebugBridge.IDeviceChangeListener):
    u'''
    Waiting until device is connected.
    '''

    TIMEOUT_UNTIL_CONNECTED_SECONDS = 10

    def __init__(self, serial_number):
        u'''
        Constructor.

        Parameters:
            serial_number : Target device that is connected. None is OK.
        '''
        self.__event = Event()
        self.__serial_number = serial_number

    def deviceConnected(self, device):
        if not self.__serial_number or device.getSerialNumber() == self.__serial_number:
            self.__event.set()

    def wait(self):
        self.__event.wait(self.TIMEOUT_UNTIL_CONNECTED_SECONDS)

def run_tests(adb_location, serial_number,
        package_name, test_runner_name, enable_coverage, coverage_file):
    u'''
    Run tests and output result as XML.

    Parameters:
        adb_location : Location of adb.
        serial_number : Serial number of device or emulator. None is OK.
        test_runner_name : Name of test runner. None is OK.
        enable_coverage : Whether coverage measuring is enabled.
        coverage_file : Path of file that will be saved coverage result.
            None is OK.
    Return:
        ElementTree of result. None if tests did not run.
    '''
    AndroidDebugBridge.init(False)

    try:
        # Connect to Android debug bridge.
        connecting_event = DeviceConnectingEvent(serial_number)
        AndroidDebugBridge.addDeviceChangeListener(connecting_event)
        debug_bridge = AndroidDebugBridge.createBridge(adb_location, False)

        # Wait until device is connected.
        connecting_event.wait()
        if not debug_bridge.isConnected():
            print >>sys.stderr, u'bridge is not connected.'
            return None

        # Get the device.
        device = get_device(serial_number, debug_bridge)
        if not device:
            print >>sys.stderr, u'There is not device.'
            return None

        # Run the test runner on the device.
        test_runner = RemoteAndroidTestRunner(
            package_name, test_runner_name, device)
        test_runner.setCoverage(enable_coverage)
        if enable_coverage and coverage_file:
            test_runner.addInstrumentationArg('coverageFile', coverage_file)
        formatter = TestResultXmlFormatter(device.getProperties())
        test_runner.run([formatter])

        return formatter.get_result()
    finally:
        # Disconnect from Android debug bridge.
        AndroidDebugBridge.terminate()

def output_result(result, file):
    u'''
    Output result to the file object.

    Parameters :
        result : An ElementTree object.
        file : File object to output result.
    '''
    # Generate XML.
    output = TemporaryFile()
    result.write(output, XML_ENCODING)

    # Format XML.
    output.seek(0)
    reader = codecs.getreader(XML_ENCODING)(output)
    outputted_xml = PATTERN_XML_INSERTING_NEW_LINE.sub(
        REPLACEMENT_XML_INSERTING_NEW_LINE, reader.read())
    output.close()

    # Output XML to the file.
    file_output = codecs.getwriter(XML_ENCODING)(file)
    file_output.write(outputted_xml)

def main():
    # Create OptionParser.
    parser = OptionParser(usage=u'usage: %prog -a ADB -s SERIAL [--coverage] [-o FILE] test_package_name [test_runner]')
    parser.add_option('-a', '--adb', metavar='ADB', dest='adb_location',
        help='Location of adb. (required)')
    parser.add_option('-b', '--adbdevicearg', metavar='ARG', dest='adb_device_arg',
        help='Arguments for adb. This option for build script by Ant.')
    parser.add_option('-f', '--coverageFile', metavar='PATH', dest='coverage_file',
        help='Path of file that will be saved coverage result on device or emulator.',
        default=None)
    parser.add_option('-s', '--serial', metavar='SERIAL', dest='serial_number',
        help='Serial number of the device. If no serial number, this script will use first device of list.')
    parser.add_option('--coverage', action='store_true', dest='coverage',
        default=False, help='Measure coverage while tests are running.')
    parser.add_option('-o', '--output', metavar='FILE', dest='output',
        help='File path of output. If this option is not specified, this script outputs to standard output.')

    # Parse command line arguments.

    (options, args) = parser.parse_args()

    if not options.adb_location:
        parser.print_help()
        sys.exit(1)

    if 1 < len(args):
        package_name = args[0]
        test_runner = args[1]
    elif 1 == len(args):
        package_name = args[0]
        test_runner = None
    else:
        parser.print_help()
        sys.exit(1)

    serial_number = None
    if options.serial_number:
        serial_number = options.serial_number
    elif options.adb_device_arg:
        serial_number = get_serial_number(options.adb_device_arg)

    output_file_name = options.output
    if output_file_name:
        try:
            output_file = file(output_file_name, 'w')
        except IOError:
            print >>sys.stderr, u'%s cannot be opened.' % (output_file_name)
            sys.exit(1)
    else:
        output_file = sys.stdout

    # Run tests.

    result = run_tests(options.adb_location, serial_number,
        package_name, test_runner, options.coverage, options.coverage_file)

    # If test is finished, output result.
    # Otherwise test running is failed.

    if result:
        output_result(result, output_file)
        status = 0
    else:
        print >>sys.stderr, u'Test was not ran.'
        status = 1

    if output_file != sys.stdout:
        output_file.close()

    sys.exit(status)

if __name__ == '__main__':
    main()

