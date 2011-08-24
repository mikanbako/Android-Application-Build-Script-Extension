#!/usr/bin/env python
# coding: UTF-8
import validate_test_text_result as validator

import unittest

class TestExtractTargetResult(unittest.TestCase):
    def test_empty(self):
        ''' Test about empty list. '''
        self.assertEquals(validator.extract_target_result('temp', []), [])

    def test_target_only(self):
        ''' Test about the list contains a line only. '''
        target_name = 'target'
        lines = [target_name + ':']

        self.assertEqual(
                validator.extract_target_result(target_name, lines), lines)

    def test_two_target(self):
        ''' Test about the list contains two targets.
        The one of targets is extracted.
        '''
        target_name = 'target'
        lines = ['other:', '  [exec] ...', target_name + ':', ' [exec] ...']

        self.assertEqual(validator.extract_target_result(target_name, lines),
                lines[2:])

    def test_three_target(self):
        ''' Test about the list contains three targets.
        The one of targets is extracted.
        '''
        target_name = 'target'
        lines = ['other1:', '   [exec] ...',
                target_name + ':', '  [exec] ...',
                'other2:']

        self.assertEqual(validator.extract_target_result(target_name, lines),
                lines[2:4])

class TestIsSucceeded(unittest.TestCase):
    def test_empty(self):
        ''' Test when the list is empty. '''
        self.assertFalse(validator.is_succeeded([]))

    def test_crashed(self):
        ''' Test when the test is crashed. '''
        self.assertFalse(validator.is_succeeded([validator.TARGET_RUN_TESTS + ':']))

    def test_ok_one_test(self):
        ''' Test when a test is OK. '''
        result_text = '''run-tests:
     [echo] Running tests ...
     [exec]
     [exec] com.example.testapp.SampleTest:.
     [exec] Test results for InstrumentationTestRunner=.
     [exec] Time: 0.02
     [exec]
     [exec] OK (1 test)
     [exec]
     [exec]
'''

        self.assertTrue(validator.is_succeeded(result_text.splitlines()))

    def test_ok_two_tests(self):
        ''' Test when two tests are OK. '''
        result_text = '''run-tests:
     [echo] Running tests ...
     [exec]
     [exec] com.example.testapp.SampleTest:..
     [exec] Test results for InstrumentationTestRunner=..
     [exec] Time: 0.06
     [exec]
     [exec] OK (2 tests)
     [exec]
     [exec]
'''

        self.assertTrue(validator.is_succeeded(result_text.splitlines()))

    def test_failures(self):
        ''' Test when the test failed. '''
        result_text = '''run-tests:
     [echo] Running tests ...
     [exec]
     [exec] com.example.testapp.SampleTest:.
     [exec] Failure in testFailure:
     [exec] junit.framework.AssertionFailedError
     [exec]      at com.example.testapp.SampleTest.testFailure(SampleTest.java:7)
     [exec]      at java.lang.reflect.Method.invokeNative(Native Method)
     [exec]      at android.test.AndroidTestRunner.runTest(AndroidTestRunner.java:169)
     [exec]      at android.test.AndroidTestRunner.runTest(AndroidTestRunner.java:154)
     [exec]      at android.test.InstrumentationTestRunner.onStart(InstrumentationTestRunner.java:529)
     [exec]      at android.app.Instrumentation$InstrumentationThread.run(Instrumentation.java:1448)
     [exec]
     [exec] Test results for InstrumentationTestRunner=..F
     [exec] Time: 0.095
     [exec]
     [exec] FAILURES!!!
     [exec] Tests run: 2,  Failures: 1,  Errors: 0
     [exec]
     [exec]
'''

        self.assertFalse(validator.is_succeeded(result_text.splitlines()))

if __name__ == '__main__':
    unittest.main()