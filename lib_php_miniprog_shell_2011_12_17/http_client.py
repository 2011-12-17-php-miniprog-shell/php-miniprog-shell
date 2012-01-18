# -*- mode: python; coding: utf-8 -*-
#
# Copyright 2011, 2012 Andrej A Antonov <polymorphm@gmail.com>.
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

import threading
import functools
import urllib.parse
import tornado.ioloop, tornado.stack_context
from .curl.request import Request

TOR_PROXY = 'localhost:9050'
TOR_PROXY_TYPE = 'socks5.hostname'

def http_post_request(host, path, data,
        use_https=None, use_tor=None, callback=None):
    if use_https is None:
        use_https = False
    if use_tor is None:
        use_tor = False
    
    if use_tor:
        proxy = TOR_PROXY
        proxy_type = TOR_PROXY_TYPE
    else:
        proxy = None
        proxy_type = None
    if use_https:
        protocol = 'https'
    else:
        protocol = 'http'
    url = '{}://{}{}'.format(protocol, host, path)
    data_str = urllib.parse.urlencode(data)
    
    request = Request(url, data=data_str, proxy=proxy, proxy_type=proxy_type)
    
    @tornado.stack_context.wrap
    def on_response(response, error):
        if error is not None:
            raise error
        
        if callback is not None:
            callback(response)
    
    def daemon():
        response = None
        error = None
        
        try:
            response = request.perform()
        except Exception as e:
            error = e
        
        tornado.ioloop.IOLoop.instance().add_callback(
                functools.partial(on_response, response, error))
    
    thread = threading.Thread(target=daemon)
    thread.daemon = True
    thread.start()
