#!/usr/bin/env python
"""
Unittests for TemporaryEnvironment function(s)
"""

from __future__ import division

import os
import unittest

from Utils.TemporaryEnvironment import set_env


class TemporaryEnvironmentTest(unittest.TestCase):
    """
    unittest for IteratorTools functions
    """

    def testSetEnv(self):
        """
        Test the grouper function (returns chunk of an iterable)
        """

        with set_env(NEW_ENV_VAR=u'blah'):
            self.assertTrue('NEW_ENV_VAR' in os.environ)
            self.assertEquals(os.environ['NEW_ENV_VAR'], u'blah')
        self.assertFalse('NEW_ENV_VAR' in os.environ)


if __name__ == '__main__':
    unittest.main()
