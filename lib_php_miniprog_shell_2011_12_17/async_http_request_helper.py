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

import urllib.parse
import tornado.httpclient

REQUEST_TIMEOUT = 1200.0

def http_post_request(host, path, data,
        use_https=None, proxy_host=None, proxy_port=None,
        callback=None):
    if use_https is None:
        use_https = False
    
    if use_https:
        protocol = 'https'
    else:
        protocol = 'http'
    
    url = '{}://{}{}'.format(protocol, host, path)
    data_str = urllib.parse.urlencode(data)
    data_b = data_str.encode()
    fetch_kwargs = {}
    if proxy_host is not None and proxy_port is not None:
        fetch_kwargs['proxy_host'] = proxy_host
        fetch_kwargs['proxy_port'] = proxy_port
    
    def on_response(response):
        response.rethrow()
        
        if callback is not None:
            callback(response)
    
    http_client = tornado.httpclient.AsyncHTTPClient()
    http_client.fetch(url, on_response,
            method='POST', body=data_b, **fetch_kwargs)
