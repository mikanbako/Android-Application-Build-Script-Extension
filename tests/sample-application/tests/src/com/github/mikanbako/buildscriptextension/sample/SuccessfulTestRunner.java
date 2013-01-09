package com.github.mikanbako.buildscriptextension.sample;

import junit.framework.TestSuite;
import android.test.InstrumentationTestRunner;

/**
 * Test runner for successful test.
 */
public class SuccessfulTestRunner extends InstrumentationTestRunner {
    @Override
    public TestSuite getAllTests() {
        // Collect tests for successful.

        TestSuite successfulSuite = new TestSuite();

        successfulSuite.addTestSuite(SuccessfulTest.class);

        return successfulSuite;
    }
}
