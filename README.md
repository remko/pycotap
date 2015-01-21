# [pycotap: Tiny Python TAP Test Runner](https://el-tramo.be/pycotap)

`pycotap` is a simple Python test runner for ``unittest`` that outputs 
[Test Anything Protocol](http://testanything.org) results to standard output 
(similar to what [`tape`](https://www.npmjs.com/package/tape) does for JavaScript).

Contrary to other TAP runners for Python, `pycotap` ...

- ... prints TAP (and *only* TAP) to standard output instead of to a separate file,
  allowing you to pipe it directly to TAP pretty printers and processors 
	(such as the ones listed on
  the [`tape` page](https://www.npmjs.com/package/tape#pretty-reporters)). By
	piping it to other consumers, you can avoid the need to add 
  specific test runners to your test code. Since the TAP results
  are printed as they come in, the consumers can directly display results while 
	the tests are run.
- ... only contains a TAP reporter, so no parsers, no frameworks, no dependencies, ...


## Installation

You can install the package directly from [PIP](https://pypi.python.org):

    pip install pycotap

Alternatively, you can build and install the package yourself:

    python setup.py install

Since the module just consists of one file, you can also just drop the file into
your project somewhere.


## Usage

Create a test suite, and pass it to a `TAPTestRunner`.
For example:

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

Running the test prints the TAP results to standard output:

    $ python ./test_example.py 
    not ok 1 __main__.MyTests.test_that_it_fails
    ok 2 __main__.MyTests.test_that_it_passes
    ok 3 __main__.MyTests.test_that_it_skips # Skipped: not finished yet
    1..3
    
Alternatively, you can pipe the test to any TAP pretty printer, such as
[faucet](https://github.com/substack/faucet) or 
[tap-dot](https://github.com/scottcorgan/tap-dot):

    $ python ./test_example.py  | faucet
    ⨯ __main__.MyTests.test_that_it_fails
    ✓ __main__.MyTests.test_that_it_passes
    ✓ __main__.MyTests.test_that_it_skips # Skipped: not finished yet
    ⨯ fail  1


    $ python ./test_example.py  | tap-dot 
    x  ..  

      3 tests
      2 passed
      1 failed  

      Failed Tests:   There was 1 failure
        x __main__.MyTests.test_that_it_fails


## API

### `TAPTestRunner()`

No constructor arguments.
