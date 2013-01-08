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
from cStringIO import StringIO

from rulesengine import InvalidNodeSizeException
from restycodes import (RESTYARGS, RestyCodes, ConditionHandler,
                        InvalidConditionNameException, getCodeStatus,)


class TestRestyCodes(unittest.TestCase):
    """
    Tests for the RestyCodes class.
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
        self.__runTest(4, 401, {'authorized': False,
                                'acceptExists': True})

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
        self.__runTest(11, 501, {'commonMethod': False,
                                 'knownMethod': False})

    def test_methodAllowedOnResource(self):
        self.__runTest(11, 405, {'methodAllowedOnResource': False})

    def test_acceptExists(self):
        self.__runTest(27, 200, {'acceptExists': True})#, calls=True)

    def test_acceptMediaTypeAvaliable(self):
        self.__runTest(13, 406, {'acceptExists': True,
                                 'acceptMediaTypeAvaliable': False})

    def test_acceptLanguageExists(self):
        self.__runTest(27, 200, {'acceptLanguageExists': True})#, calls=True)

    def test_acceptLanguageAvaliable(self):
        self.__runTest(14, 406, {'acceptLanguageExists': True,
                                 'acceptLanguageAvaliable': False})

    def test_acceptCharacterSetExists(self):
        self.__runTest(27, 200, {'acceptCharacterSetExists': True})

    def test_acceptCharacterSetAvaliable(self):
        self.__runTest(15, 406, {'acceptCharacterSetExists': True,
                                 'acceptCharacterSetAvaliable': False})

    def test_acceptEncodingExists(self):
        self.__runTest(27, 200, {'acceptEncodingExists': True})

    def test_acceptEncodingAvaliable(self):
        self.__runTest(16, 406, {'acceptEncodingExists': True,
                                 'acceptEncodingAvaliable': False})

    #@skip(SKIP_MESSAGE)
    def test_resourceExists(self):
        self.__runTest(26, 200, {'resourceExists': True}, calls=False)
        self.__runTest(20, 404, {'resourceExists': False}, calls=False)

    #@skip(SKIP_MESSAGE)
    def test_ifMatchExists(self):
        self.__runTest(28, 200, {'resourceExists': True,
                                'ifMatchExists': True}, calls=False)

    #@skip(SKIP_MESSAGE)
    def test_ifMatchAnyExists(self):
        self.__runTest(27, 200, {'resourceExists': True,
                                 'ifMatchExists': True,
                                 'ifMatchAnyExists': True}, calls=False)
        self.__runTest(28, 200, {'resourceExists': True,
                                'ifMatchExists': True,
                                'ifMatchAnyExists': False}, calls=False)
        self.__runTest(17, 412, {'resourceExists': False,
                                 'ifMatchAnyExists': True}, calls=False)

    def test_eTagInMatch(self):
        self.__runTest(19, 412, {'resourceExists': True,
                                 'ifMatchExists': True,
                                 'ifMatchAnyExists': False,
                                 'eTagInMatch': False}, calls=False)
        self.__runTest(28, 200, {'resourceExists': True,
                                 'ifMatchExists': True,
                                 'ifMatchAnyExists': False,
                                 'eTagInMatch': True}, calls=False)

    #@skip(SKIP_MESSAGE)
    def test_ifUnmodifiedSinceExists(self):
        self.__runTest(27, 200, {'resourceExists': True,
                                 'ifUnmodifiedSinceExists': True}, calls=False)

    #@skip(SKIP_MESSAGE)
    def test_ifUnmodifiedSinceIsValidDate(self):
        self.__runTest(28, 200, {'resourceExists': True,
                                'ifUnmodifiedSinceExists': True,
                                'ifUnmodifiedSinceIsValidDate': True},
                       calls=False)

    def test_lastModifiedGtIfUnmodifiedSince(self):
        self.__runTest(20, 412, {'resourceExists': True,
                                 'ifUnmodifiedSinceExists': True,
                                 'ifUnmodifiedSinceIsValidDate': True,
                                 'lastModifiedGtIfUnmodifiedSince': True})
        self.__runTest(28, 200, {'resourceExists': True,
                                 'ifUnmodifiedSinceExists': True,
                                 'ifUnmodifiedSinceIsValidDate': True,
                                 'lastModifiedGtIfUnmodifiedSince': False})

    def test_put(self):
        self.__runTest(27, 200, {'resourceExists': True,
                                 'put': True})
        self.__runTest(21, 201, {'resourceExists': False,
                                 'put': True})

    def test_applyToDifferentURI(self):
        self.__runTest(19, 301, {'resourceExists': False,
                                 'put': True,
                                 'applyToDifferentURI': True})

    def test_conflict(self):
        self.__runTest(24, 409, {'resourceExists': True,
                                 'put': True,
                                 'conflict': True})
        self.__runTest(20, 409, {'resourceExists': False,
                                 'put': True,
                                 'conflict': True})#, calls=True)

    def test_newResourceCreated(self):
        self.__runTest(22, 202, {'resourceExists': False,
                                 'put': True,
                                 'newResourceCreated': False})#, calls=True)
        self.__runTest(24, 202, {'resourceExists': False,
                                 'post': True,
                                 'newResourceCreated': False})#, calls=True)

    def test_resourcePreviouslyExisted(self):
        self.__runTest(22, 410, {'resourceExists': False,
                                 'resourcePreviouslyExisted': True})

    def test_resourceMovedPermanently(self):
        self.__runTest(20, 301, {'resourceExists': False,
                                 'resourcePreviouslyExisted': True,
                                 'resourceMovedPermanently': True})

    def test_resourceMovedTemporarily(self):
        self.__runTest(21, 307, {'resourceExists': False,
                                 'resourcePreviouslyExisted': True,
                                 'resourceMovedTemporarily': True})

    #@skip(SKIP_MESSAGE)
    def test_post(self):
        self.__runTest(23, 201, {'resourceExists': False,
                                 'post': True})
        self.__runTest(25, 201, {'resourceExists': False,
                                 'resourcePreviouslyExisted': True,
                                 'post': True})#, calls=True)

    def test_permitPostToMissingResource(self):
        self.__runTest(21, 404, {'resourceExists': False,
                                 'post': True,
                                 'permitPostToMissingResource': False},
                       calls=False)
        self.__runTest(23, 410, {'resourceExists': False,
                                 'resourcePreviouslyExisted': True,
                                 'post': True,
                                 'permitPostToMissingResource': False},
                       calls=False)

    def test_redirect(self):
        self.__runTest(23, 303, {'resourceExists': True,
                                 'post': True,
                                 'redirect': True}, calls=False)
        self.__runTest(23, 303, {'resourceExists': True,
                                 'resourcePreviouslyExisted': True,
                                 'post': True,
                                 'permitPostToMissingResource': True,
                                 'redirect': True}, calls=False)
        self.__runTest(23, 303, {'resourceExists': True,
                                 'post': True,
                                 'permitPostToMissingResource': True,
                                 'redirect': True}, calls=False)

    #@skip(SKIP_MESSAGE)
    def test_ifNoneMatchExists(self):
        self.__runTest(28, 200, {'resourceExists': True,
                                 'ifNoneMatchExists': True}, calls=False)

    #@skip(SKIP_MESSAGE)
    def test_ifNoneMatchAnyExists(self):
        self.__runTest(21, 304, {'resourceExists': True,
                                 'ifNoneMatchExists': True,
                                 'ifNoneMatchAnyExists': True}, calls=False)
        self.__runTest(28, 200, {'resourceExists': True,
                                 'ifNoneMatchExists': True,
                                 'ifNoneMatchAnyExists': False}, calls=False)

    #@skip(SKIP_MESSAGE)
    def test_eTagInIfNoneMatch(self):
        self.__runTest(22, 304, {'resourceExists': True,
                                'ifNoneMatchExists': True,
                                'eTagInIfNoneMatch': True}, calls=False)
        self.__runTest(28, 200, {'resourceExists': True,
                                'ifNoneMatchExists': True,
                                'eTagInIfNoneMatch': False}, calls=False)

    def test_getOrHead(self):
        self.__runTest(21, 304, {'resourceExists': True,
                                 'ifNoneMatchExists': True,
                                 'ifNoneMatchAnyExists': True,
                                 'getOrHead': True}, calls=False)
        self.__runTest(21, 412, {'resourceExists': True,
                                 'ifNoneMatchExists': True,
                                 'ifNoneMatchAnyExists': True,
                                 'getOrHead': False}, calls=False)
        self.__runTest(22, 304, {'resourceExists': True,
                                 'ifNoneMatchExists': True,
                                 'eTagInIfNoneMatch': True,
                                 'getOrHead': True}, calls=False)
        self.__runTest(22, 412, {'resourceExists': True,
                                 'ifNoneMatchExists': True,
                                 'eTagInIfNoneMatch': True,
                                 'getOrHead': False}, calls=False)

    #@skip(SKIP_MESSAGE)
    def test_ifModifiedSinceExists(self):
        self.__runTest(27, 200, {'resourceExists': True,
                                 'ifModifiedSinceExists': True}, calls=False)

    #@skip(SKIP_MESSAGE)
    def test_ifModifiedSinceIsValidDate(self):
        self.__runTest(27, 200, {'resourceExists': True,
                                 'ifModifiedSinceExists': True,
                                 'ifModifiedSinceIsValidDate': False},
                       calls=False)
        self.__runTest(28, 200, {'resourceExists': True,
                                 'ifModifiedSinceExists': True,
                                 'ifModifiedSinceIsValidDate': True},
                       calls=False)

    #@skip(SKIP_MESSAGE)
    def test_ifModifiedSinceGtNow(self):
        self.__runTest(29, 200, {'resourceExists': True,
                                 'ifModifiedSinceExists': True,
                                 'ifModifiedSinceIsValidDate': True,
                                 'ifModifiedSinceGtNow': False}, calls=False)
        self.__runTest(28, 200, {'resourceExists': True,
                                 'ifModifiedSinceExists': True,
                                 'ifModifiedSinceIsValidDate': True,
                                 'ifModifiedSinceGtNow': True}, calls=False)

    def test_lastModifiedGtIfModifiedSince(self):
        self.__runTest(23, 304, {'resourceExists': True,
                                 'ifModifiedSinceExists': True,
                                 'ifModifiedSinceIsValidDate': True,
                                 'ifModifiedSinceGtNow': False,
                                 'lastModifiedGtIfModifiedSince': False})
        self.__runTest(29, 200, {'resourceExists': True,
                                 'ifModifiedSinceExists': True,
                                 'ifModifiedSinceIsValidDate': True,
                                 'ifModifiedSinceGtNow': False,
                                 'lastModifiedGtIfModifiedSince': True})

    #@skip(SKIP_MESSAGE)
    def test_delete(self):
        self.__runTest(24, 200, {'resourceExists': True,
                                 'delete': True}, calls=False)
        self.__runTest(26, 200, {'resourceExists': True,
                                'delete': False}, calls=False)

    def test_methodEnacted(self):
        self.__runTest(22, 202, {'resourceExists': True,
                                 'delete': True,
                                 'methodEnacted': False}, calls=False)

    def test_responseIncludesAnEntity(self):
        self.__runTest(22, 204, {'resourceExists': False,
                                 'put': True,
                                 'newResourceCreated': False,
                                 'responseIncludesAnEntity': False},
                       calls=False)
        self.__runTest(23, 204, {'resourceExists': True,
                                 'delete': True,
                                 'responseIncludesAnEntity': False},
                       calls=False)

    def test_multipleRepresentation(self):
        self.__runTest(24, 300, {'resourceExists': True,
                                 'delete': True,
                                 'multipleRepresentation': True})#, calls=True)
        self.__runTest(26, 300, {'resourceExists': True,
                                 'post': True,
                                 'multipleRepresentation': True})#, calls=True)
        self.__runTest(27, 300, {'resourceExists': True,
                                 'put': True,
                                 'multipleRepresentation': True})#, calls=True)
        self.__runTest(26, 300, {'resourceExists': True,
                                 'multipleRepresentation': True})#, calls=True)

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
            print

            for call in seq:
                print call.__name__

            print "Total Count: {0}".format(len(seq))


class TestConditionHandler(unittest.TestCase):
    """
    Tests for the ConditionHandler class.
    """
    def __init__(self, name):
        """
        :Parameters:
          name : str
            Unit test name.
        """
        super(TestConditionHandler, self).__init__(name)

    def setUp(self):
        """
        Create the RestyCodes instance.
        """
        self._ch = ConditionHandler()

    def tearDown(self):
        pass

    def test_requestUrlTooLong(self):
        for size, code in ((20, 200), (19, 200), (18, 414)):
            self._ch.requestUrlTooLong("someverylongurl.com", size)
            self.__runTest(code, "with size: {0}".format(size))

    def test_requestEntityTooLarge(self):
        rawEntity = StringIO()
        rawEntity.write("GET / http/1.1\r\n")
        rawEntity.write("Host: example.org\r\n")
        rawEntity.write("\r\n")
        rawEntity.write("Some entity body text.\r\n")
        result = rawEntity.getvalue()
        rawEntity.close()

        for size, code in ((62, 200), (61, 200), (60, 413)):
            self._ch.requestEntityTooLarge(result, size)
            self.__runTest(code, "with size: {0}".format(size))

    def test_method(self):
        for method, code in (('DELETE', 200), ('GET', 200), ('HEAD', 200),
                             ('PUT', 200), ('POST', 200), ('OPTIONS', 200),
                             ('TRACE', 405), ('CONNECT', 405), ('MOVE', 405),
                             ('PROPPATCH', 405), ('MKCOL', 405), ('COPY', 405),
                             ('UNLOCK', 405), ('UNKNOWN', 501)):
            self._ch.method(method)
            self.__runTest(code, "with method: {0}".format(method))







    def __runTest(self, code, message=""):
        msg = "Invalid status: found {0}, should be {1}"
        found = self._ch.getStatus()
        status = getCodeStatus(code)
        msg += ", " + message
        self.assertTrue(found == status, msg.format(found, status))


if __name__ == '__main__':
    unittest.main()
