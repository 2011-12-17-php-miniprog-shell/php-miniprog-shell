# -*- mode: python; coding: utf-8 -*-
#
# Copyright 2012 Andrej A Antonov <polymorphm@gmail.com>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

assert str is not bytes

from ctypes import *
import ctypes.util

curl = None

_curl_name = ctypes.util.find_library('curl')

if _curl_name is not None:
    try:
        curl = CDLL(_curl_name)
    except EnvironmentError:
        pass
else:
    try:
        curl = cdll.libcurl
    except EnvironmentError:
        pass

if curl is None:
    raise ImportError('cannot open shared object file')

# types

CURL_HANDLE = c_void_p
curl_slist_p = c_void_p
CURLcode = c_int
CURLoption = c_int
CURLINFO = c_int

WRITEFUNCTION = CFUNCTYPE(c_size_t, POINTER(c_char), c_size_t, c_size_t, c_void_p)

# consts

CURL_GLOBAL_ALL = 3

CURLOPT_ERRORBUFFER = 10010
CURLOPT_URL = 10002
CURLOPT_WRITEFUNCTION = 20011
CURLOPT_WRITEDATA = 10001
CURLOPT_POSTFIELDS = 10015
CURLOPT_POSTFIELDSIZE_LARGE = 30120
CURLOPT_HTTPHEADER = 10023
CURLOPT_PROXY = 10004
CURLOPT_PROXYTYPE = 101

CURLPROXY_HTTP = 0
CURLPROXY_HTTP_1_0 = 1
CURLPROXY_SOCKS4 = 4
CURLPROXY_SOCKS5 = 5
CURLPROXY_SOCKS4A = 6
CURLPROXY_SOCKS5_HOSTNAME = 7

CURLINFO_RESPONSE_CODE = 2097154

# errors

ERRORS_MAP = {
    0: 'CURLE_OK',
    1: 'CURLE_UNSUPPORTED_PROTOCOL',
    2: 'CURLE_FAILED_INIT',
    3: 'CURLE_URL_MALFORMAT',
    4: 'CURLE_NOT_BUILT_IN',
    5: 'CURLE_COULDNT_RESOLVE_PROXY',
    6: 'CURLE_COULDNT_RESOLVE_HOST',
    7: 'CURLE_COULDNT_CONNECT',
    22: 'CURLE_HTTP_RETURNED_ERROR',
    34: 'CURLE_HTTP_POST_ERROR',
    35: 'CURLE_SSL_CONNECT_ERROR',
    41: 'CURLE_FUNCTION_NOT_FOUND',
    42: 'CURLE_ABORTED_BY_CALLBACK',
    43: 'CURLE_BAD_FUNCTION_ARGUMENT',
    45: 'CURLE_INTERFACE_FAILED',
    47: 'CURLE_TOO_MANY_REDIRECTS',
    48: 'CURLE_UNKNOWN_OPTION',
    51: 'CURLE_PEER_FAILED_VERIFICATION',
    52: 'CURLE_GOT_NOTHING',
    53: 'CURLE_SSL_ENGINE_NOTFOUND',
    54: 'CURLE_SSL_ENGINE_SETFAILED',
    55: 'CURLE_SEND_ERROR',
    56: 'CURLE_RECV_ERROR',
    58: 'CURLE_SSL_CERTPROBLEM',
    59: 'CURLE_SSL_CIPHER',
    60: 'CURLE_SSL_CACERT',
    80: 'CURLE_SSL_SHUTDOWN_FAILED',
    88: 'CURLE_CHUNK_FAILED',
}

# prototypes

curl_global_init = CFUNCTYPE(CURLcode, c_long)(curl.curl_global_init)
curl_easy_init = CFUNCTYPE(CURL_HANDLE)(curl.curl_easy_init)
curl_easy_cleanup = CFUNCTYPE(None, CURL_HANDLE)(curl.curl_easy_cleanup)
curl_slist_append = CFUNCTYPE(curl_slist_p, curl_slist_p, c_char_p)(curl.curl_slist_append)
curl_slist_free_all = CFUNCTYPE(None, curl_slist_p)(curl.curl_slist_free_all)
curl_easy_setopt__c_long = CFUNCTYPE(CURLcode, CURL_HANDLE, CURLoption, c_long)(curl.curl_easy_setopt)
curl_easy_setopt__c_char_p = CFUNCTYPE(CURLcode, CURL_HANDLE, CURLoption, c_char_p)(curl.curl_easy_setopt)
curl_easy_setopt__writefunction = CFUNCTYPE(CURLcode, CURL_HANDLE, CURLoption, WRITEFUNCTION)(curl.curl_easy_setopt)
curl_easy_setopt__c_void_p = CFUNCTYPE(CURLcode, CURL_HANDLE, CURLoption, c_void_p)(curl.curl_easy_setopt)
curl_easy_perform = CFUNCTYPE(CURLcode, CURL_HANDLE)(curl.curl_easy_perform)
curl_easy_getinfo__pointer_c_long = CFUNCTYPE(CURLcode, CURL_HANDLE, CURLINFO, POINTER(c_long))(curl.curl_easy_getinfo)

# run init

curl_global_init(CURL_GLOBAL_ALL)
