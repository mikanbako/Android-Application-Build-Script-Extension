package com.github.mikanbako.buildscriptextension.sample;

import junit.framework.Assert;
import junit.framework.TestCase;

/**
 * Test class for failure test.
 */
public class FailureTest extends TestCase {
    /**
     * Test for failure.
     *
     * This test must be failure.
     */
    public void testFailure() {
        Assert.assertEquals("This test is for failure.",
                1, TestedClass.add(1, 1));
    }
}
