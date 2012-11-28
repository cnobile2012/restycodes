#
# restycodes/resty_codes.py
#
"""
Resty Codes
  Returns a (code, 'Description') tuple derived from data that was supplied
  from an application. This code implements the diagram by Alan Dean at:
  http://code.google.com/p/http-headers-status/.

by: Carl J. Nobile

email: carl.nobile@gmail.com
"""
__docformat__ = "restructuredtext en"


from rulesengine import RulesEngine


STATUS_CODE_MAP = {
    # Informational
    100: "Continue",
    101: "Switching Protocols",
    102: "Processing",
    103: "Access denied while creating Web Service",
    104: "File Format or Program Error",
    # Successful
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    207: "Multi-Status",
    226: "IM Used",
    # Redirection
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    306: "Switch Proxy",
    307: "Temporary Redirect",
    # Client Error
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Time-out",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Request Entity Too Large",
    414: "Request-URI Too Large",
    415: "Unsupported Media Type",
    416: "Requested range not satisfiable",
    417: "Expectation Failed",
    418: "Resume Incomplete",
    419: "Insufficient Space On Resource",
    420: "Method Failure",
    421: "Bad Mapping",
    422: "Unprocessable Entity",
    423: "Locked",
    424: "Failed Dependency",
    425: "No Code",
    426: "Upgrade Required",
    # Server Error
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Time-out",
    505: "HTTP Version not supported",
    506: "Variant also negotiates",
    507: "Insufficient Storage",
    508: "Cross Server Binding Forbidden",
    509: "Bandwidth Exceeded",
    510: "Not Extended",
    999: "Undefined (Converted to a 200 OK)",
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
    'resourceExists': False,
    'ifMatchExists': False,
    'ifMatchAnyExists': False,
    'eTagInMatch': True,
    'ifUnmodifiedSinceExists': False,
    'ifUnmodifiedSinceIsValidDate': False,
    'lastModifiedGtIfUnmodifiedSince': False,
    'put': False,
    'applyToDifferentURI': False,
    'conflict': False,
    'newResource': True,
    'resourcePreviouslyExisted': False,
    'resourceMovedPermanently': False,
    'resourceMovedTemporarily': False,
    'post': True,
    'permitPostToMissingResource': True,
    'redirect': False,
    }


class RestyCodesException(Exception): pass
class InvalidConditionNameException(RestyCodesException): pass


class RestyCodes(RulesEngine):
    """
    All internal method calls shall return a Boolean.
    """
    DEFAULT_CODE = 999
    COMMON_METHODS = ('DELETE', 'GET', 'HEAD', 'PUT', 'POST',)
    KNOWN_METHODS = ('TRACE', 'CONNECT', 'MOVE', 'PROPPATCH', 'MKCOL',
                     'COPY', 'UNLOCK',)

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

        for key, value in kwargs.items():
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
        return kwargs.get('resourceExists', False)

    def _ifMatchExists(self, **kwargs):
        return kwargs.get('ifMatchExists', False)

    def _ifMatchAnyExists(self, **kwargs):
        resource = kwargs.get('resourceExists', False)
        result = kwargs.get('ifMatchAnyExists', False)
        if not resource: self._code = result and 412 or self.DEFAULT_CODE
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

    def _newResource(self, **kwargs):
        result = kwargs.get('newResource', True)
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
        result = kwargs.get('post', True)
        resource = kwargs.get('resourcePreviouslyExisted', False)
        if resource: self._code = result and self.DEFAULT_CODE or 410
        else: self._code = result and self.DEFAULT_CODE or 404
        return result

    def _permitPostToMissingResource(self, **kwargs):
        result = kwargs.get('permitPostToMissingResource', True)
        resource = kwargs.get('resourcePreviouslyExisted', False)
        if resource: self._code = result and self.DEFAULT_CODE or 410
        else: self._code = result and self.DEFAULT_CODE or 404
        return result

    def _redirect(self, **kwargs):
        result = kwargs.get('redirect', False)
        self._code = result and 303 or self.DEFAULT_CODE
        return result






    # [callable,
    #  True -- (callable|None),
    #  False -- (callable|None)]



    # New Resource
    nodeNewResource = [_newResource,
                       None,
                       None]
    # Redirect
    nodeRedirect = [_redirect,
                    None,
                    nodeNewResource]

    # If Modified Since Exists
    nodeIfUnmodifiedSinceExists = [_ifUnmodifiedSinceExists,
                                   [_ifUnmodifiedSinceIsValidDate,
                                    [_lastModifiedGtIfUnmodifiedSince,
                                     None,
                                     None],
                                    None],
                                   None]

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
                              nodeNewResource]],
                            [_resourcePreviouslyExisted,
                              [_resourceMovedPermanently,
                               None,
                               [_resourceMovedTemporarily,
                                None,
                                [_post,
                                 [_permitPostToMissingResource,
                                  nodeRedirect,
                                  None],
                                 None]]],
                              [_post,
                               [_permitPostToMissingResource,
                                nodeRedirect,
                                None],
                               None]]]]]

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
