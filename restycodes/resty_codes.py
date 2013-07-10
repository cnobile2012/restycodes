#
# restycodes/resty_codes.py
#
"""
Resty Codes
  Returns a (code, 'Description') tuple derived from data that was supplied
  from an application. This code is based on the diagram by Alan Dean at:
  http://code.google.com/p/http-headers-status/.

  I have drawn a new diagram which comes with this package.

by: Carl J. Nobile

email: carl.nobile@gmail.com
"""
__docformat__ = "restructuredtext en"


from rulesengine import RulesEngine


STATUS_CODE_MAP = {
    # Informational
    100: "Continue",                               # Not implemented (RFC-2616)
    101: "Switching Protocols",                    # Not implemented (RFC-2616)
    102: "Processing",                             # Not implemented (RFC-2518)
    103: "Access denied while creating Web Service", # Not implemented
    104: "File Format or Program Error",           # Not implemented
    # Successful
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-Authoritative Information",          # Not implemented (RFC-2616)
    204: "No Content",
    205: "Reset Content",                          # Not implemented (RFC-2616)
    206: "Partial Content",                        # Not implemented (RFC-2616)
    207: "Multi-Status",                           # Not implemented (RFC-4918)
    208: "Already Reported",                       # Not implemented (RFC-5842)
    226: "IM Used",                                # Not implemented (RFC-3229)
    # Redirection
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",                                  # Not implemented (RFC-2616)
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",                              # Not implemented (RFC-2616)
    306: "Unused",                  # [Switch Proxy] Not implemented (RFC-2616)
    307: "Temporary Redirect",
    # Client Error
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",                       # Not implemented (RFC-2616)
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",          # Not implemented (RFC-2616)
    408: "Request Timeout",                        # Not implemented (RFC-2616)
    409: "Conflict",
    410: "Gone",
    411: "Length Required",                        # Not implemented (RFC-2616)
    412: "Precondition Failed",
    413: "Request Entity Too Large",
    414: "Request-URI Too Large",
    415: "Unsupported Media Type",
    416: "Requested range not satisfiable",        # Not implemented (RFC-2616)
    417: "Expectation Failed",                     # Not implemented (RFC-2616)
    418: "Resume Incomplete", # I'm a teapot (RFC-2324) Not implemented (Internet draft)
    419: "Insufficient Space On Resource",   # Not implemented (Internet draft)
    420: "Policy not Fulfilled",         # Not implemented (WD-http-pep-971121)
    421: "Bad Mapping",                  # Not implemented (WD-http-pep-971121)
    422: "Unprocessable Entity",                   # Not implemented (RFC-4918)
    423: "Locked",                                 # Not implemented (RFC-4918)
    424: "Failed Dependency",     # [Method Failure] Not implemented (RFC-4918)
    425: "No Code",                          # Not implemented (Internet draft)
    426: "Upgrade Required",                       # Not implemented (RFC-2817)
    428: "Precondition Required",                  # Not implemented (RFC-6585)
    429: "Too Many Requests",                      # Not implemented (RFC-6585)
    431: "Request Header Fields Too Large",        # Not implemented (RFC-6585)
    451: "Unavailable For Legal Reasons",    # Not implemented (Internet draft)
    # Server Error
    500: "Internal Server Error",                  # Not implemented (RFC-2616)
    501: "Not Implemented",
    502: "Bad Gateway",                            # Not implemented (RFC-2616)
    503: "Service Unavailable",
    504: "Gateway Timeout",                        # Not implemented (RFC-2616)
    505: "HTTP Version not supported",             # Not implemented (RFC-2616)
    506: "Variant also negotiates",                # Not implemented (RFC-2295)
    507: "Insufficient Storage",                   # Not implemented (RFC-4918)
    508: "Cross Server Binding Forbidden",         # Not implemented (RFC-5842)
    509: "Bandwidth Exceeded",                     # Not implemented (None)
    510: "Not Extended",                           # Not implemented (RFC 2774)
    511: "Network Authentication Required",        # Not implemented (RFC 6585)
    999: "Undefined",                              # RestyCodes internal only
    }


def getCodeStatus(code):
    '''
    Get a `tuple` of the response. ex. ``(200, "OK")``.

    :Parameters:
      code : `int`
        The HTTP response code.

    :Returns:
      A `tuple` of the response
    '''
    return (code, STATUS_CODE_MAP.get(code, ""))


RESTYARGS = {
    'serviceAvailable': True,
    'requestUrlTooLong': False,
    'badRequest': False,
    'authorized': True,
    'forbidden': False,
    'notImplemented': False,
    'unsupportedMediaType': False,
    'requestEntityTooLarge': False,
    'options': False,
    'commonMethod': True,
    'knownMethod': True,
    'methodAllowedOnResource': True,
    'acceptExists': False,
    'acceptMediaTypeAvaliable': True,
    'acceptLanguageExists': False,
    'acceptLanguageAvaliable': True,
    'acceptCharacterSetExists': False,
    'acceptCharacterSetAvaliable': True,
    'acceptEncodingExists': False,
    'acceptEncodingAvaliable': True,
    'resourceExists': True,
    'ifMatchExists': False,
    'ifMatchAnyExists': False,
    'eTagInMatch': True,
    'ifUnmodifiedSinceExists': False,
    'ifUnmodifiedSinceIsValidDate': False,
    'lastModifiedGtIfUnmodifiedSince': False,
    'put': False,
    'applyToDifferentURI': False,
    'conflict': False,
    'newResourceCreated': True,
    'resourcePreviouslyExisted': False,
    'resourceMovedPermanently': False,
    'resourceMovedTemporarily': False,
    'post': False,
    'permitPostToMissingResource': True,
    'redirect': False,
    'ifNoneMatchExists': False,
    'ifNoneMatchAnyExists': False,
    'eTagInIfNoneMatch': False,
    'getOrHead': True,
    'ifModifiedSinceExists': False,
    'ifModifiedSinceIsValidDate': False,
    'ifModifiedSinceGtNow': True,
    'lastModifiedGtIfModifiedSince': True,
    'delete': False,
    'methodEnacted': True,
    'responseIncludesAnEntity': True,
    'multipleRepresentation': False,
    }


class RestyCodesException(Exception): pass
class InvalidConditionNameException(RestyCodesException): pass


class RestyCodes(RulesEngine):
    """
    All internal method calls shall return a Boolean.
    """
    DEFAULT_CODE = 999

    def __init__(self, storeSeq=False):
        """
        Instantiates the `RulesEngine` and calls its load method.
        """
        super(RestyCodes, self).__init__(storeSeq=storeSeq)
        self.load(self.nodeTree)
        self._code = self.DEFAULT_CODE

    def getStatus(self, **kwargs):
        """
        Gets the status after it runs the ``RulesEngine dump`` method.

        :Parameters:
          kwargs : `dict`
            The keyword arguments that are passed to the internal method calls.
        """
        self.dump(**kwargs)
        return getCodeStatus(self._code)

    def setConditions(self, **kwargs):
        """
        Set key/value pairs in a copy of `RESTYARGS`. This method checks that
        the keyword exists in `RESTYARGS` before setting the value.

        *Example*
          ``kwargs`` = ``{'authorized': False, 'acceptExists': True}``

        :Parameters:
          kwargs : `dict`
            The keyword values that will replace the values in the copy of
            `RESTYARGS`.

        :Returns:
          A keyword argument dict suitable for passing to the `getStatus`
          method.
        """
        restyArgs = dict(RESTYARGS)

        for key, value in list(kwargs.items()):
            if key not in RESTYARGS:
                msg = "Provided key '{0}' is not in kwargs.".format(key)
                raise InvalidConditionNameException(msg)

            restyArgs[key] = value

        return restyArgs

    #
    # Internal method calls.
    #
    def _serviceAvailable(self, **kwargs):
        result = kwargs.get('serviceAvailable', True)
        self._code = result and self.DEFAULT_CODE or 503
        return result

    def _requestUrlTooLong(self, **kwargs):
        result = kwargs.get('requestUrlTooLong', False)
        self._code = result and 414 or self.DEFAULT_CODE
        return result

    def _badRequest(self, **kwargs):
        result = kwargs.get('badRequest', False)
        self._code = result and 400 or self.DEFAULT_CODE
        return result

    def _authorized(self, **kwargs):
        result = kwargs.get('authorized', True)
        self._code = result and self.DEFAULT_CODE or 401
        return result

    def _forbidden(self, **kwargs):
        result = kwargs.get('forbidden', False)
        self._code = result and 403 or self.DEFAULT_CODE
        return result

    def _notImplemented(self, **kwargs):
        result = kwargs.get('notImplemented', False)
        self._code = result and 501 or self.DEFAULT_CODE
        return result

    def _unsupportedMediaType(self, **kwargs):
        result = kwargs.get('unsupportedMediaType', False)
        self._code = result and 415 or self.DEFAULT_CODE
        return result

    def _requestEntityTooLarge(self, **kwargs):
        result = kwargs.get('requestEntityTooLarge', False)
        self._code = result and 413 or self.DEFAULT_CODE
        return result

    def _options(self, **kwargs):
        result = kwargs.get('options', False)
        self._code = result and 200 or self.DEFAULT_CODE
        return result

    def _commonMethod(self, **kwargs):
        return kwargs.get('commonMethod', True)

    def _methodAllowedOnResource(self, **kwargs):
        result = kwargs.get('methodAllowedOnResource', True)
        self._code = result and self.DEFAULT_CODE or 405
        return result

    def _knownMethod(self, **kwargs):
        result = kwargs.get('knownMethod', True)
        self._code = result and 405 or 501
        return result

    def _acceptExists(self, **kwargs):
        return kwargs.get('acceptExists', False)

    def _acceptMediaTypeAvaliable(self, **kwargs):
        result = kwargs.get('acceptMediaTypeAvaliable', True)
        self._code = result and self.DEFAULT_CODE or 406
        return result

    def _acceptLanguageExists(self, **kwargs):
        return kwargs.get('acceptLanguageExists', False)

    def _acceptLanguageAvaliable(self, **kwargs):
        result = kwargs.get('acceptLanguageAvaliable', True)
        self._code = result and self.DEFAULT_CODE or 406
        return result

    def _acceptCharacterSetExists(self, **kwargs):
        return kwargs.get('acceptCharacterSetExists', False)

    def _acceptCharacterSetAvaliable(self, **kwargs):
        result = kwargs.get('acceptCharacterSetAvaliable', True)
        self._code = result and self.DEFAULT_CODE or 406
        return result

    def _acceptEncodingExists(self, **kwargs):
        return kwargs.get('acceptEncodingExists', False)

    def _acceptEncodingAvaliable(self, **kwargs):
        result = kwargs.get('acceptEncodingAvaliable', True)
        self._code = result and self.DEFAULT_CODE or 406
        return result

    def _resourceExists(self, **kwargs):
        return kwargs.get('resourceExists', True)

    def _ifMatchExists(self, **kwargs):
        return kwargs.get('ifMatchExists', False)

    def _ifMatchAnyExists(self, **kwargs):
        result = kwargs.get('ifMatchAnyExists', False)

        if not kwargs.get('resourceExists', False):
            self._code = result and 412 or self.DEFAULT_CODE

        return result

    def _eTagInMatch(self, **kwargs):
        result = kwargs.get('eTagInMatch', True)
        self._code = result and self.DEFAULT_CODE or 412
        return result

    def _ifUnmodifiedSinceExists(self, **kwargs):
        return kwargs.get('ifUnmodifiedSinceExists', False)

    def _ifUnmodifiedSinceIsValidDate(self, **kwargs):
        return kwargs.get('ifUnmodifiedSinceIsValidDate', False)

    def _lastModifiedGtIfUnmodifiedSince(self, **kwargs):
        result = kwargs.get('lastModifiedGtIfUnmodifiedSince', False)
        self._code = result and 412 or self.DEFAULT_CODE
        return result

    def _put(self, **kwargs):
        return kwargs.get('put', False)

    def _applyToDifferentURI(self, **kwargs):
        result = kwargs.get('applyToDifferentURI', False)
        self._code = result and 301 or self.DEFAULT_CODE
        return result

    def _conflict(self, **kwargs):
        result = kwargs.get('conflict', False)
        self._code = result and 409 or self.DEFAULT_CODE
        return result

    def _newResourceCreated(self, **kwargs):
        result = kwargs.get('newResourceCreated', True)
        self._code = result and 201 or self.DEFAULT_CODE
        return result

    def _resourcePreviouslyExisted(self, **kwargs):
        return kwargs.get('resourcePreviouslyExisted', False)

    def _resourceMovedPermanently(self, **kwargs):
        result = kwargs.get('resourceMovedPermanently', False)
        self._code = result and 301 or self.DEFAULT_CODE
        return result

    def _resourceMovedTemporarily(self, **kwargs):
        result = kwargs.get('resourceMovedTemporarily', False)
        self._code = result and 307 or self.DEFAULT_CODE
        return result

    def _post(self, **kwargs):
        result = kwargs.get('post', False)

        if not kwargs.get('resourceExists', False):
            if kwargs.get('resourcePreviouslyExisted', False):
                self._code = result and self.DEFAULT_CODE or 410
            else:
                self._code = result and self.DEFAULT_CODE or 404

        return result

    def _permitPostToMissingResource(self, **kwargs):
        result = kwargs.get('permitPostToMissingResource', True)

        if kwargs.get('resourcePreviouslyExisted', False):
            self._code = result and self.DEFAULT_CODE or 410
        else:
            self._code = result and self.DEFAULT_CODE or 404

        return result

    def _redirect(self, **kwargs):
        result = kwargs.get('redirect', False)
        self._code = result and 303 or self.DEFAULT_CODE
        return result

    def _ifNoneMatchExists(self, **kwargs):
        return kwargs.get('ifNoneMatchExists', False)

    def _ifNoneMatchAnyExists(self, **kwargs):
        return kwargs.get('ifNoneMatchAnyExists', False)

    def _eTagInIfNoneMatch(self, **kwargs):
        return kwargs.get('eTagInIfNoneMatch', False)

    def _getOrHead(self, **kwargs):
        result = kwargs.get('getOrHead', True)
        self._code = result and 304 or 412
        return result

    def _ifModifiedSinceExists(self, **kwargs):
        return kwargs.get('ifModifiedSinceExists', False)

    def _ifModifiedSinceIsValidDate(self, **kwargs):
        return kwargs.get('ifModifiedSinceIsValidDate', False)

    def _ifModifiedSinceGtNow(self, **kwargs):
        return kwargs.get('ifModifiedSinceGtNow', True)

    def _lastModifiedGtIfModifiedSince(self, **kwargs):
        result = kwargs.get('lastModifiedGtIfModifiedSince', True)
        self._code = result and self.DEFAULT_CODE or 304
        return result

    def _delete(self, **kwargs):
        return kwargs.get('delete', False)

    def _methodEnacted(self, **kwargs):
        result = kwargs.get('methodEnacted', True)
        self._code = result and self.DEFAULT_CODE or 202
        return result

    def _responseIncludesAnEntity(self, **kwargs):
        result = kwargs.get('responseIncludesAnEntity', True)

        if kwargs.get('delete', False):
            self._code = result and self.DEFAULT_CODE or 204
        else:
            self._code = result and 202 or 204

        return result

    def _multipleRepresentation(self, **kwargs):
        result = kwargs.get('multipleRepresentation', False)
        self._code = result and 300 or 200
        return result

    # [callable,
    #  [callable, ..., ...] or None, (True branch)
    #  [callable, ..., ...] or None  (False branch)
    # ]

    # Method Enacted
    nodeMethodEnacted = [_methodEnacted,
                         [_responseIncludesAnEntity,
                          [_multipleRepresentation,
                           None,
                           None],
                          None],
                         None]

    # New Resource Created
    nodeNewResourceCreated = [_newResourceCreated,
                              None,
                              [_responseIncludesAnEntity,
                               None,
                               None]]

    # Post
    nodePost = [_post,
                [_permitPostToMissingResource,
                 [_redirect,
                  None,
                  nodeNewResourceCreated],
                 None],
                None]

    # Delete
    nodeDelete = [_delete,
                  nodeMethodEnacted,
                  [_post,
                   [_redirect,
                    None,
                    nodeMethodEnacted],
                   [_put,
                    [_conflict,
                     None,
                     nodeMethodEnacted],
                    nodeMethodEnacted]]]

    # If Modified Since Exists
    nodeIfModifiedSinceExists = [_ifModifiedSinceExists,
                                 [_ifModifiedSinceIsValidDate,
                                  [_ifModifiedSinceGtNow,
                                   nodeDelete,
                                   [_lastModifiedGtIfModifiedSince,
                                    nodeDelete,
                                    None]],
                                  nodeDelete],
                                 nodeDelete]

    # If None Match Exists
    nodeIfNoneMatchExists = [_ifNoneMatchExists,
                             [_ifNoneMatchAnyExists,
                              [_getOrHead,
                               None,
                               None],
                              [_eTagInIfNoneMatch,
                               [_getOrHead,
                                None,
                                None],
                               nodeIfModifiedSinceExists]],
                             nodeIfModifiedSinceExists]

    # If Modified Since Exists
    nodeIfUnmodifiedSinceExists = [_ifUnmodifiedSinceExists,
                                   [_ifUnmodifiedSinceIsValidDate,
                                    [_lastModifiedGtIfUnmodifiedSince,
                                     None,
                                     nodeIfNoneMatchExists],
                                    nodeIfNoneMatchExists],
                                   nodeIfNoneMatchExists]

    # Resource Exists
    nodeResourceExists = [_resourceExists,
                          [_ifMatchExists,
                           [_ifMatchAnyExists,
                            nodeIfUnmodifiedSinceExists,
                            [_eTagInMatch,
                             nodeIfUnmodifiedSinceExists,
                             None]],
                           nodeIfUnmodifiedSinceExists],
                          [_ifMatchAnyExists,
                           None,
                           [_put,
                            [_applyToDifferentURI,
                             None,
                             [_conflict,
                              None,
                              nodeNewResourceCreated]],
                            [_resourcePreviouslyExisted,
                             [_resourceMovedPermanently,
                              None,
                              [_resourceMovedTemporarily,
                               None,
                               nodePost]],
                             nodePost]]]]

    # Accept Encoding
    nodeAcceptEncoding = [_acceptEncodingExists,
                          [_acceptEncodingAvaliable,
                           nodeResourceExists,
                           None],
                          nodeResourceExists]

    # Accept Character Set
    nodeAcceptCharacterSet = [_acceptCharacterSetExists,
                              [_acceptCharacterSetAvaliable,
                               nodeAcceptEncoding,
                               None],
                              nodeAcceptEncoding]

    # Accept Language
    nodeAcceptLanguage = [_acceptLanguageExists,
                          [_acceptLanguageAvaliable,
                           nodeAcceptCharacterSet,
                           None],
                          nodeAcceptCharacterSet]

    # Main Tree
    nodeTree = [_serviceAvailable,
                [_requestUrlTooLong,
                 None,
                 [_badRequest,
                  None,
                  [_authorized,
                   [_forbidden,
                    None,
                    [_notImplemented,
                     None,
                     [_unsupportedMediaType,
                      None,
                      [_requestEntityTooLarge,
                       None,
                       [_options,
                        None,
                        [_commonMethod,
                         [_methodAllowedOnResource,
                          [_acceptExists,
                           [_acceptMediaTypeAvaliable,
                            nodeAcceptLanguage,
                            None],
                           nodeAcceptLanguage],
                          None],
                         [_knownMethod, None, None]]]]]]],
                   None]]],
                None]


class ConditionHandler(RestyCodes):
    """
    Defines some basic methods that generate results satisfying the
    requirements of the conditions in the RestyCodes class.
    """
    COMMON_METHODS = ('DELETE', 'GET', 'HEAD', 'PUT', 'POST',)
    KNOWN_METHODS = ('TRACE', 'CONNECT', 'MOVE', 'PROPPATCH', 'MKCOL',
                     'COPY', 'UNLOCK',)

    def __init__(self, storeSeq=False):
        super(ConditionHandler, self).__init__(storeSeq=storeSeq)
        self._kwargs = {}

    def getStatus(self):
        kwargs = self.setConditions(**self._kwargs)
        return super(ConditionHandler, self).getStatus(**kwargs)

    def requestUrlTooLong(self, url, size):
        self._kwargs['requestUrlTooLong'] = len(url) > size

    def requestEntityTooLarge(self, entity, size):
        self._kwargs['requestEntityTooLarge'] = len(entity) > size

    def method(self, method):
        self._kwargs['options'] = method.upper() == 'OPTIONS'
        self._kwargs['commonMethod'] = method.upper() in self.COMMON_METHODS
        self._kwargs['knownMethod'] = method.upper() in self.KNOWN_METHODS
