#!/usr/bin/env python

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import unittest
import StringIO

from pycotap import TAPTestRunner, LogMode

class TAPTestRunnerTest(unittest.TestCase):
  def setUp(self):
    self.output_stream = StringIO.StringIO()
    self.error_stream = StringIO.StringIO()

  def run_test(self, test_class, **kwargs):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    return TAPTestRunner(output_stream = self.output_stream, error_stream = self.error_stream, **kwargs).run(suite)

  def test_all_test_outcomes(self):
    class Test(unittest.TestCase) :
    # class Test(object) :
      def test_passing(self):
        self.assertEqual(1, 1)
      def test_failing(self):
        self.assertEqual(1, 2)
      @unittest.skip("Not finished yet")
      def test_skipped(self):
        self.assertEqual(1, 2)

    self.run_test(Test)
    self.assertEqual(self.output_stream.getvalue(), (
      "TAP version 13\n"
      "not ok 1 __main__.Test.test_failing\n"
      "ok 2 __main__.Test.test_passing\n"
      "ok 3 __main__.Test.test_skipped # SKIP Not finished yet\n"
      "1..3\n"
    ))
    self.assertEqual("", self.error_stream.getvalue())

  def test_log_to_diagnostics(self):
    class Test(unittest.TestCase) :
      def test_output(self):
        print "Foo"
        sys.stderr.write("Baz\n")
        print "Bar"

    self.run_test(Test)
    self.assertEqual(self.output_stream.getvalue(), (
      "TAP version 13\n"
      "ok 1 __main__.Test.test_output\n"
      "# Foo\n"
      "# Baz\n"
      "# Bar\n"
      "1..1\n"
    ))
    self.assertEqual("", self.error_stream.getvalue())

  def test_log_to_error(self):
    class Test(unittest.TestCase) :
      def test_output(self):
        print "Foo"
        sys.stderr.write("Baz\n")
        print "Bar"

    self.run_test(Test, log_mode = LogMode.LogToError)
    self.assertEqual(self.output_stream.getvalue(), (
      "TAP version 13\n"
      "ok 1 __main__.Test.test_output\n"
      "1..1\n"
    ))
    self.assertEqual(self.error_stream.getvalue(), (
      "Foo\n"
      "Baz\n"
      "Bar\n"
    ))

  def test_log_to_error_order(self):
    class Test(unittest.TestCase) :
      def test_output(self):
        print "Foo"
        sys.stderr.write("Baz\n")
        print "Bar"

    self.output_stream = self.error_stream
    self.run_test(Test, log_mode = LogMode.LogToError)
    self.assertEqual(self.output_stream.getvalue(), (
      "TAP version 13\n"
      "Foo\n"
      "Baz\n"
      "Bar\n"
      "ok 1 __main__.Test.test_output\n"
      "1..1\n"
    ))


if __name__ == '__main__':
  # unittest.main()
  TAPTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TAPTestRunnerTest))
