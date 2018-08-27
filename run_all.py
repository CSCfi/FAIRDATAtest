import sys
import unittest
from os.path import dirname

from HtmlTestRunner import HTMLTestRunner


print('-- Starting Fairdata tests --')

loader = unittest.TestLoader()
start_dir = dirname(__file__)

# tests are only automatically searched from files whose filenames end with *_tests.py
suite = loader.discover(start_dir, pattern='*_tests.py')

if sys.argv[-1] == '--runner=default':
    # HTMLTestRunner does not seem to forward print() -clauses to stdout.
    # it may be useful to use unittest's default TextTestRunner for debugging.
    runner = unittest.TextTestRunner()
else:
    runner = HTMLTestRunner(output='reports', report_name='fairdata_integration_tests', combine_reports=True)

runner.run(suite)
