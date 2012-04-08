#!/usr/bin/env python
import logging
import sys
from os.path import dirname, abspath
from optparse import OptionParser
from unittest import TextTestRunner

logging.getLogger('cardgameengine').addHandler(logging.StreamHandler())

sys.path.insert(0, dirname(abspath(__file__)))


def runtests(*test_args, **kwargs):
    test_runner = TextTestRunner(**kwargs)
    failures = test_runner.run_tests(test_args)
    sys.exit(failures)

if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()

    runtests(*args, **options.__dict__)

