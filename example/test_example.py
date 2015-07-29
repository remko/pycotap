#!/usr/bin/env python
# pylint: disable=C0325

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import unittest

class MyTests(unittest.TestCase):
  def test_that_it_passes(self):
    print("First line of output")
    print("Second line of output")
    self.assertEqual(0, 0)

  @unittest.skip("Not finished yet")
  def test_that_it_skips(self): 
    raise Exception("Does not happen")

  def test_that_it_fails(self):
    print("First line of output")
    print("Second line of output")
    self.assertEqual(1, 0)

  def test_that_an_error_occurs(self):
    print("Something is about to happen")
    raise Exception("Something bad happened")

  @unittest.expectedFailure
  def test_that_is_expected_to_fail(self):
    print("This test is expected to fail")
    self.assertEqual(1, 0)

  @unittest.expectedFailure
  def test_with_unexpected_success(self):
    print("This test has an unexpected success")
    self.assertEqual(1, 1)
  

if __name__ == '__main__':
  from pycotap import TAPTestRunner, LogMode
  suite = unittest.TestLoader().loadTestsFromTestCase(MyTests)
  TAPTestRunner(message_log = LogMode.LogToYAML, test_output_log = LogMode.LogToDiagnostics).run(suite)
