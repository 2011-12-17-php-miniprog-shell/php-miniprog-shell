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
from . import lib

class RequestError(IOError):
    pass

def curl_func_or_error(curl_func, *args, **kwargs):
    res = curl_func(*args, **kwargs)
    
    if res:
        strerror = lib.ERRORS_MAP.get(res)
        if strerror is not None:
            msg = 'curl error code {!r}: {}'.format(res, strerror)
        else:
            msg = 'curl error code {!r} (see http://curl.haxx.se/libcurl/c/libcurl-errors.html)'.format(res)
        
        error = RequestError(msg)
        error.curl_error_code = res
        raise error

class EasyCurl:
    def __init__(self):
        self.handle = lib.curl_easy_init()
    def __del__(self):
        try:
            header_slist_opt = self.header_slist_opt
        except AttributeError:
            pass
        else:
            lib.curl_slist_free_all(header_slist_opt)
            del self.header_slist_opt
        
        try:
            handle = self.handle
        except AttributeError:
            pass
        else:
            lib.curl_easy_cleanup(handle)
            del self.handle

def get_response_status(curl_obj):
    code = c_long(0)
    
    curl_func_or_error(lib.curl_easy_getinfo__pointer_c_long,
            curl_obj.handle, lib.CURLINFO_RESPONSE_CODE, pointer(code))
    
    return code.value

class ResponseResult:
    pass

class Request:
    def __init__(self, url, data=None, header_list=None, proxy=None, proxy_type=None):
        self._curl_obj = EasyCurl()
        
        # options for threadsafe perform
        curl_func_or_error(lib.curl_easy_setopt__c_long,
                self._curl_obj.handle, lib.CURLOPT_NOSIGNAL, 1)
        curl_func_or_error(lib.curl_easy_setopt__c_long,
                self._curl_obj.handle, lib.CURLOPT_DNS_USE_GLOBAL_CACHE, 0)
        
        self._curl_obj.url_opt = c_char_p(url.encode())
        curl_func_or_error(lib.curl_easy_setopt__c_char_p,
                self._curl_obj.handle, lib.CURLOPT_URL, self._curl_obj.url_opt)
        
        self._curl_obj.write_func_opt = lib.WRITEFUNCTION(self._on_write)
        curl_func_or_error(lib.curl_easy_setopt__writefunction,
                self._curl_obj.handle, lib.CURLOPT_WRITEFUNCTION, self._curl_obj.write_func_opt)
        
        if data is not None:
            if isinstance(data, str):
                data = data.encode()
            
            self._curl_obj.post_fields_opt = pointer(create_string_buffer(len(data)))
            self._curl_obj.post_fields_opt.contents.value = data
            
            curl_func_or_error(lib.curl_easy_setopt__c_long,
                    self._curl_obj.handle, lib.CURLOPT_POSTFIELDSIZE_LARGE,
                    sizeof(self._curl_obj.post_fields_opt.contents))
            curl_func_or_error(lib.curl_easy_setopt__c_void_p,
                    self._curl_obj.handle, lib.CURLOPT_POSTFIELDS, self._curl_obj.post_fields_opt)
        
        if header_list is not None:
            self._curl_obj.header_slist_opt = lib.curl_slist_p()
            
            for header in header_list:
                if isinstance(header, str):
                    header = header.encode()
                
                self._curl_obj.header_slist_opt = lib.curl_slist_append(
                        self._curl_obj.header_slist_opt, header)
            
            curl_func_or_error(lib.curl_easy_setopt__c_void_p,
                    self._curl_obj.handle, lib.CURLOPT_HTTPHEADER, self._curl_obj.header_slist_opt)
        
        if proxy is not None:
            self._curl_obj.proxy_opt = c_char_p(proxy.encode())
            curl_func_or_error(lib.curl_easy_setopt__c_char_p,
                    self._curl_obj.handle, lib.CURLOPT_PROXY, self._curl_obj.proxy_opt)
        
        if proxy_type is not None:
            proxy_type_code = {
                'http': lib.CURLPROXY_HTTP,
                'http1.0': lib.CURLPROXY_HTTP_1_0,
                'socks4': lib.CURLPROXY_SOCKS4,
                'socks5': lib.CURLPROXY_SOCKS5,
                'socks4a': lib.CURLPROXY_SOCKS4A,
                'socks5.hostname': lib.CURLPROXY_SOCKS5_HOSTNAME,
            }.get(proxy_type)
            
            if proxy_type_code is None:
                raise NotImplementedError('not supported proxy type {!r}'.format(proxy_type))
            
            curl_func_or_error(lib.curl_easy_setopt__c_long,
                    self._curl_obj.handle, lib.CURLOPT_PROXYTYPE, proxy_type_code)
    
    def _on_write(self, ptr, size, nmemb, userdata):
        real_size = size * nmemb
        
        if not real_size:
            return 0
        
        buf_p = cast(ptr, POINTER(c_char * real_size))
        buf = bytes(buf_p.contents)
        
        self._response_contents.append(buf)
        
        return real_size
    
    def perform(self):
        self._response_contents = []
        
        curl_func_or_error(lib.curl_easy_perform, self._curl_obj.handle)
        
        response = ResponseResult()
        response.status = get_response_status(self._curl_obj)
        response.contents = b''.join(self._response_contents)
        
        return response
