#!/usr/bin/env python
#
# restycodes/tests.py
#
"""
Test Resty Codes
  Unit test for the resty codes API.

by: Carl J. Nobile

email: carl.nobile@gmail.com
"""
__docformat__ = "restructuredtext en"


import unittest
from unittest import skip

from rulesengine import InvalidNodeSizeException
from restycodes import RESTYARGS, RestyCodes, InvalidConditionNameException


class TestRestyCodes(unittest.TestCase):
    """
    Tests for the rules engine.
    """
    SKIP_MESSAGE = "This test will fail until all conditions are implemented."

    def __init__(self, name):
        """
        :Parameters:
          name : str
            Unit test name.
        """
        super(TestRestyCodes, self).__init__(name)

    def setUp(self):
        """
        Create the RestyCodes instance.
        """
        self._rc = RestyCodes(storeSeq=True)

    def tearDown(self):
        pass

    def testSetConditions(self):
        # Test for an invalid keyword arg.
        replacements = {'wrongArg': False}
        self.assertRaises(InvalidConditionNameException,
                          self._rc.setConditions,
                          **replacements)
        # Test for proper operation.
        self.__runTest(4, 401, {'authorized': False, 'acceptExists': True})

    def test_serviceAvailable(self):
        self.__runTest(1, 503, {'serviceAvailable': False})

    def test_requestUrlTooLong(self):
        self.__runTest(2, 414, {'requestUrlTooLong': True})

    def test_badRequest(self):
        self.__runTest(3, 400, {'badRequest': True})

    def test_authorized(self):
        self.__runTest(4, 401, {'authorized': False})

    def test_forbidden(self):
        self.__runTest(5, 403, {'forbidden': True})

    def test_notImplemented(self):
        self.__runTest(6, 501, {'notImplemented': True})

    def test_unsupportedMediaType(self):
        self.__runTest(7, 415, {'unsupportedMediaType': True})

    def test_requestEntityTooLarge(self):
        self.__runTest(8, 413, {'requestEntityTooLarge': True})

    def test_options(self):
        self.__runTest(9, 200, {'options': True})

    def test_commonMethod(self):
        self.__runTest(11, 405, {'commonMethod': False})

    def test_knownMethod(self):
        self.__runTest(11, 501, {'commonMethod': False, 'knownMethod': False})

    def test_methodAllowedOnResource(self):
        self.__runTest(11, 405, {'methodAllowedOnResource': False})

    @skip(SKIP_MESSAGE)
    def test_acceptExists(self):
        self.__runTest(0, 999, {'acceptExists': True, 'c999to200': False})

    def test_acceptMediaTypeAvaliable(self):
        self.__runTest(13, 406, {'acceptExists': True,
                                 'acceptMediaTypeAvaliable': False})

    @skip(SKIP_MESSAGE)
    def test_acceptLanguageExists(self):
        self.__runTest(0, 999, {'acceptLanguageExists': True,
                                 'c999to200': False})

    def test_acceptLanguageAvaliable(self):
        self.__runTest(14, 406, {'acceptLanguageExists': True,
                                 'acceptLanguageAvaliable': False})

    @skip(SKIP_MESSAGE)
    def test_acceptCharacterSetExists(self):
        self.__runTest(0, 999, {'acceptCharacterSetExists': True,
                                 'c999to200': False})

    def test_acceptCharacterSetAvaliable(self):
        self.__runTest(15, 406, {'acceptCharacterSetExists': True,
                                 'acceptCharacterSetAvaliable': False})

    @skip(SKIP_MESSAGE)
    def test_acceptEncodingExists(self):
        self.__runTest(0, 999, {'acceptEncodingExists': True,
                                 'c999to200': False})

    def test_acceptEncodingAvaliable(self):
        self.__runTest(16, 406, {'acceptEncodingExists': True,
                                 'acceptEncodingAvaliable': False})

    @skip(SKIP_MESSAGE)
    def test_resourceExists(self):
        self.__runTest(0, 999, {'resourceExists': True,
                                 'c999to200': False})

    @skip(SKIP_MESSAGE)
    def test_ifMatchExists(self):
        self.__runTest(0, 999, {'resourceExists': True})
        self.__runTest(0, 999, {'resourceExists': True, 'ifMatchExist': True})

    @skip(SKIP_MESSAGE)
    def test_ifMatchAnyExists(self):
        self.__runTest(17, 412, {'ifMatchAnyExists': True})
        self.__runTest(0, 999, {'resourceExists': True,
                                'ifMatchExists': True,
                                'c999to200': False}, calls=True)
        self.__runTest(0, 999, {'resourceExists': True,
                                'ifMatchExists': True,
                                'ifMatchAnyExists': False,
                                'c999to200': False})

    def test_eTagInMatch(self):
        self.__runTest(19, 412, {'resourceExists': True,
                                 'ifMatchExists': True,
                                 'ifMatchAnyExists': False,
                                 'eTagInMatch': False})

    @skip(SKIP_MESSAGE)
    def test_ifUnmodifiedSinceExists(self):
        self.__runTest(0, 999, {'ifUnmodifiedSinceExists': True,
                                'c999to200': False})

    @skip(SKIP_MESSAGE)
    def test_ifUnmodifiedSinceIsValidDate(self):
        self.__runTest(0, 999, {'ifUnmodifiedSinceExists': True,
                                'ifUnmodifiedSinceIsValidDate': True,
                                'c999to200': False})

    def test_lastModifiedGtIfUnmodifiedSince(self):
        self.__runTest(20, 412, {'resourceExists': True,
                                 'ifUnmodifiedSinceExists': True,
                                 'ifUnmodifiedSinceIsValidDate': True,
                                 'lastModifiedGtIfUnmodifiedSince': True})

    @skip(SKIP_MESSAGE)
    def test_put(self):
        self.__runTest(0, 999, {'put': True})

    #def test_







    def __runTest(self, expect, code, condition, calls=False):
        kwargs = self._rc.setConditions(**condition)
        result = self._rc.getStatus(**kwargs)
        count = self._rc.getIterationCount()
        self.__printCalls(calls=calls)
        msg = "Iteration count should be {0}, but found {1}".format(
            expect, count)
        self.assertTrue(count == expect, msg)
        msg = "Status code should be {0}, but found {1}".format(
            code, result[0])
        self.assertTrue(result[0] == code, msg)

    def __printCalls(self, calls=False):
        if calls:
            seq = self._rc.getCallSequence()

            for call in seq:
                print call.__name__

            print "Total Count: {0}".format(len(seq))

if __name__ == '__main__':
    unittest.main()
