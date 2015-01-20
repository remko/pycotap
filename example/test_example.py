import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import unittest
from pycotap import TAPTestRunner

class MyTests(unittest.TestCase):
  def test_that_it_passes(self):
    self.assertEqual(0, 0)

  @unittest.skip("not finished yet")
  def test_that_it_skips(self): 
    raise Exception("Does not happen")

  def test_that_it_fails(self):
    self.assertEqual(1, 0)

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(MyTests)
  TAPTestRunner().run(suite)
