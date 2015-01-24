#!/usr/bin/env python
# coding=utf-8

# Copyright (c) 2015 Remko Tronçon (https://el-tramo.be)
# Released under the MIT license
# See COPYING for details


import unittest
import sys
if sys.hexversion >= 0x03000000:
  from io import StringIO
else:
  from StringIO import StringIO

# Log modes
class LogMode(object) :
  LogToError, LogToDiagnostics = range(2)


class TAPTestResult(unittest.TestResult):
  def __init__(self, output_stream, error_stream, log_mode):
    super(TAPTestResult, self).__init__(self, output_stream)
    self.output_stream = output_stream
    self.error_stream = error_stream
    self.orig_stdout = None
    self.orig_stderr = None
    self.output = None
    self.log_mode = log_mode
    self.output_stream.write("TAP version 13\n")

  def print_raw(self, text):
    self.output_stream.write(text)
    self.output_stream.flush()

  def print_result(self, result, test, directive = None):
    self.output_stream.write("%s %d %s" % (result, self.testsRun, test.id()))
    if directive:
      self.output_stream.write(" # " + directive)
    self.output_stream.write("\n")
    self.output_stream.flush()

  def ok(self, test, directive = None):
    self.print_result("ok", test, directive)

  def not_ok(self, test):
    self.print_result("not ok", test)

  def startTest(self, test):
    self.orig_stdout = sys.stdout
    self.orig_stderr = sys.stderr
    if self.log_mode == LogMode.LogToDiagnostics:
      sys.stdout = sys.stderr = self.output = StringIO()
    else:
      sys.stdout = sys.stderr = self.error_stream
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
    sys.stderr.write(self.errors[-1][1] + "\n")
    self.not_ok(test)

  def addFailure(self, test, err):
    super(TAPTestResult, self).addFailure(test, err)
    sys.stderr.write(self.failures[-1][1] + "\n")
    self.not_ok(test)

  def addSkip(self, test, reason):
    super(TAPTestResult, self).addSkip(test, reason)
    self.ok(test, "SKIP " + reason)

  def addExpectedFailure(self, test, err):
    super(TAPTestResult, self).addExpectedFailure(test, err)
    sys.stderr.write(self.expectedFailures[-1][1] + "\n")
    self.ok(test)

  def addUnexpectedSuccess(self, test):
    super(TAPTestResult, self).addUnexpectedSuccess(self, test)
    self.not_ok(test)

  def printErrors(self):
    self.print_raw("1..%d\n" % self.testsRun)


class TAPTestRunner(object):
  def __init__(self, log_mode = LogMode.LogToDiagnostics, output_stream = sys.stdout, error_stream = sys.stderr):
    self.output_stream = output_stream
    self.error_stream = error_stream
    self.log_mode = log_mode

  def run(self, test):
    result = TAPTestResult(self.output_stream, self.error_stream, self.log_mode)
    test(result)
    result.printErrors()

    return result
