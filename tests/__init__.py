import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


if __name__ == '__main__':
    loader = unittest.TestLoader()
    tests = loader.discover(start_dir='tests', pattern='test_*.py')
    test_runner = unittest.runner.TextTestRunner()
    result = test_runner.run(tests)
    sys.exit(not result.wasSuccessful())
