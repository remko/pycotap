#!/usr/bin/env python
# coding=utf-8

# Copyright (c) 2015 Remko Tronçon (https://el-tramo.be)
# Released under the MIT license
# See COPYING for details

import unittest
import sys
import StringIO

# Log modes
class LogMode(object) :
  LogToError, LogToDiagnostics = range(2)


class TAPTestResult(unittest.TestResult):
  def __init__(self, stream, log_mode):
    super(TAPTestResult, self).__init__(self, stream)
    self.stream = stream
    self.orig_stdout = None
    self.orig_stderr = None
    self.output = None
    self.log_mode = log_mode
    self.stream.write("TAP version 13\n")

  def print_raw(self, text):
    self.stream.write(text)
    self.stream.flush()

  def print_result(self, result, test, directive = None):
    self.stream.write("%s %d %s" % (result, self.testsRun, test.id()))
    if directive:
      self.stream.write(" # " + directive)
    self.stream.write("\n")
    self.stream.flush()

  def ok(self, test, directive = None):
    self.print_result("ok", test, directive)

  def not_ok(self, test):
    self.print_result("not ok", test)

  def startTest(self, test):
    self.orig_stdout = sys.stdout
    self.orig_stderr = sys.stderr
    if self.log_mode == LogMode.LogToDiagnostics:
      sys.stdout = sys.stderr = self.output = StringIO.StringIO()
    else:
      sys.stdout = sys.stderr
    super(TAPTestResult, self).startTest(test)

  def stopTest(self, test):
    super(TAPTestResult, self).stopTest(test)
    sys.stdout = self.orig_stdout
    sys.stderr = self.orig_stderr
    if self.log_mode == LogMode.LogToDiagnostics:
      output = self.output.getvalue()
      if len(output):
        self.print_raw("# " + output.rstrip().replace("\n", "\n# ") + "\n")

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
  def __init__(self, log_mode = LogMode.LogToDiagnostics):
    self.stream = sys.stdout
    self.log_mode = log_mode

  def run(self, test):
    result = TAPTestResult(self.stream, self.log_mode)
    try:
      test(result)
    finally:
      pass

    result.printErrors()

    return result
