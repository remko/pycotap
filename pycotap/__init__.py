#!/usr/bin/env python
# coding=utf-8

# Copyright (c) 2015 Remko Tronçon (https://el-tramo.be)
# Released under the MIT license
# See COPYING for details

import unittest
import sys

class TAPTestResult(unittest.TestResult):
  def __init__(self, stream):
    super(TAPTestResult, self).__init__(self, stream)
    self.stream = stream
    self.orig_stdout = None
    self.stream.write("TAP version 13\n")

  def print_result(self, result, test, directive = None) :
    self.stream.write("%s %d %s" % (result, self.testsRun, test.id()))
    if directive:
      self.stream.write(" # " + directive)
    self.stream.write("\n")
    self.stream.flush()

  def ok(self, test, directive = None) :
    self.print_result("ok", test, directive)

  def not_ok(self, test) :
    self.print_result("not ok", test)

  def startTest(self, test):
    self.orig_stdout = sys.stdout
    sys.stdout = sys.stderr
    super(TAPTestResult, self).startTest(test)

  def stopTest(self, test):
    super(TAPTestResult, self).stopTest(test)
    sys.stdout = self.orig_stdout

  def addSuccess(self, test):
    super(TAPTestResult, self).addSuccess(test)
    self.ok(test)

  def addError(self, test, err):
    super(TAPTestResult, self).addError(test, err)
    self.not_ok(test)

  def addFailure(self, test, err):
    super(TAPTestResult, self).addFailure(test, err)
    self.not_ok(test)

  def addSkip(self, test, reason):
    super(TAPTestResult, self).addSkip(test, reason)
    self.ok(test, "SKIP " + reason)

  def addExpectedFailure(self, test, err):
    super(TAPTestResult, self).addExpectedFailure(test, err)
    self.ok(test)

  def addUnexpectedSuccess(self, test):
    super(TAPTestResult, self).addUnexpectedSuccess(self, test)
    self.not_ok(test)

  def printErrors(self):
    print "1..%d" % self.testsRun

class TAPTestRunner(object):
  def __init__(self):
    self.stream = sys.stdout

  def run(self, test):
    result = TAPTestResult(self.stream)
    try:
      test(result)
    finally:
      pass

    result.printErrors()

    return result
