#!/usr/bin/env python
#
# rulesengine/tests.py
#
"""
Test Rules Engine
  Unit test for the rules engine.

by: Carl J. Nobile

email: carl.nobile@gmail.com
"""
__docformat__ = "restructuredtext en"


import unittest

from rulesengine import (RulesEngine, InvalidNodeSizeException,)


class TestRulesEngine(unittest.TestCase):
    """
    Tests for the rules engine.
    """
    def __init__(self, name):
        """
        :Parameters:
          name : str
            Unit test name.
        """
        super(TestRulesEngine, self).__init__(name)

    def setUp(self):
        """
        Create the rules engine.
        """
        self._re = RulesEngine(self)

    def tearDown(self):
        pass

    def testEmptyNode(self):
        """
        Test that the ``InvalidNodeSizeException`` exception is raised when
        an empty sequence object is encountered.
        """
        self.assertRaises(InvalidNodeSizeException, self._re.load, [])

    def testShortNode(self):
        """
        Test that the ``InvalidNodeSizeException`` exception is raised when
        a too short sequence object is encountered.
        """
        self.assertRaises(InvalidNodeSizeException,
                          self._re.load, [None, None, ])

    def testLongNode(self):
        """
        Test that the ``InvalidNodeSizeException`` exception is raised when
        a too long sequence object is encountered.
        """
        self.assertRaises(InvalidNodeSizeException,
                          self._re.load, [None, None, None, None, ])

    def testLogic_01(self):
        """
        Test that the iteration count is correct for the sequence object
        configuration.
        """
        self._re.load(self.nodeTree)
        self._re.dump()
        expect = 3
        count = self._re.getIterationCount()
        msg = "Iteration count should be {0}, found {1}".format(expect, count)
        self.assertTrue(count == expect, msg)

    def testLogic_02(self):
        """
        Test that the iteration count is correct for the sequence object
        configuration.
        """
        self._re.load(self.nodeTree)
        kwargs = {'arg1': True, 'arg2': False, 'arg3': True}
        self._re.dump(**kwargs)
        expect = 3
        count = self._re.getIterationCount()
        msg = "Iteration count should be {0}, found {1}".format(expect, count)
        self.assertTrue(count == expect, msg)

    def testLogic_03(self):
        """
        Test that the iteration count is correct for the sequence object
        configuration.
        """
        self._re.load(self.nodeTree)
        kwargs = {'arg1': False, 'arg2': False, 'arg3': True}
        self._re.dump(**kwargs)
        expect = 1
        count = self._re.getIterationCount()
        msg = "Iteration count should be {0}, found {1}".format(expect, count)
        self.assertTrue(count == expect, msg)

    def testLogic_04(self):
        """
        Test that the iteration count is correct for the sequence object
        configuration.
        """
        self._re.load(self.nodeTree)
        kwargs = {'arg1': True, 'arg2': True, 'arg3': True}
        self._re.dump(**kwargs)
        expect = 2
        count = self._re.getIterationCount()
        msg = "Iteration count should be {0}, found {1}".format(expect, count)
        self.assertTrue(count == expect, msg)

    def _dummyMethod_01(self, **kwargs):
        """
        Test method 1.
        """
        return kwargs.get('arg1', True)

    def _dummyMethod_02(self, **kwargs):
        """
        Test method 2.
        """
        return kwargs.get('arg2', False)

    def _dummyMethod_03(self, **kwargs):
        """
        Test method 3.
        """
        return kwargs.get('arg3', True)

    # [callable,
    #  True -- (callable|None),
    #  False -- (callable|None)]
    nodeTree = [_dummyMethod_01,
                [_dummyMethod_02,
                 None,
                 [_dummyMethod_03,
                  None,
                  None]],
                None]


if __name__ == '__main__':
    unittest.main()
