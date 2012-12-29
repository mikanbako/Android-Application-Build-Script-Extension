package com.github.mikanbako.buildscriptextension.sample;

import junit.framework.TestSuite;
import android.test.InstrumentationTestRunner;

/**
 * Test runner for failure test.
 */
public class FailureTestRunner extends InstrumentationTestRunner {
    @Override
    public TestSuite getAllTests() {
        // Collect tests for failure.

        TestSuite failureSuite = new TestSuite();

        failureSuite.addTestSuite(FailureTest.class);

        return failureSuite;
    }
}
