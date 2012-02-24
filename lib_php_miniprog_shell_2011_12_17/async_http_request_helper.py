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

import urllib.parse, urllib.request
from .daemon_async import daemon_async

REQUEST_TIMEOUT = 1200.0
RESPONSE_BODY_LENGTH_LIMIT = 100000000

class Response:
    pass

@daemon_async
def async_fetch(url, data=None, proxies=None):
    build_opener_args = []
    if proxies is not None:
        build_opener_args.append(
                urllib.request.ProxyHandler(proxies=proxies))
    
    opener = urllib.request.build_opener(*build_opener_args)
    f = opener.open(url, data=data, timeout=REQUEST_TIMEOUT)
    
    response = Response()
    response.code = f.getcode()
    response.body = f.read(RESPONSE_BODY_LENGTH_LIMIT)
    
    return response

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
    data_b = urllib.parse.urlencode(data).encode()
    fetch_kwargs = {}
    if proxy_host is not None and proxy_port is not None:
        if ':' in proxy_host:
            proxies = {'http': '[{}]:{}'.format(proxy_host, proxy_port)}
        else:
            proxies = {'http': '{}:{}'.format(proxy_host, proxy_port)}
    else:
        proxies = None
    
    async_fetch(url, data=data_b, proxies=proxies, callback=callback)
