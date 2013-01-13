package com.github.mikanbako.buildscriptextension.sample;

import junit.framework.Assert;
import junit.framework.TestCase;

/**
 * Test class for successful test.
 */
public class SuccessfulTest extends TestCase {
    /**
     * Test for success.
     *
     * This test must be successful.
     */
    public void testSuccess() {
        Assert.assertEquals(2, TestedClass.add(1, 1));
    }
}
