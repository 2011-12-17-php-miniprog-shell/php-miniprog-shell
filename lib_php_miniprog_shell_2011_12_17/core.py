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

import base64
from .auth import gen_hash
from .async_http_request_helper import http_post_request
from .main import UserError

class RunFuncError(Exception):
    pass

class StatusRunFuncError(RunFuncError):
    pass

class DataRunFuncError(RunFuncError):
    pass

def run_func_core(host, path, hash_hex, func,
        use_https=None, proxy_host=None, proxy_port=None,
        use_response_json=None, callback=None):
    if use_response_json is None:
        use_response_json = True
    
    if isinstance(func, str):
        func = func.encode()
    
    data = {
        'hash': hash_hex,
        'func_b': base64.b64encode(func),
    }
    
    def on_response(response):
        response_data = response.body
        
        if response.code != 200:
            raise RunFuncError(
                'response.status not 200. response_data is:\n'
                '{}\n__END_RESPONSE_DATA__'.format(response_data))
        
        
        if use_response_json:
            from json import loads as json_loads
            
            try:
                response_data = json_loads(response_data.decode())
            except ValueError as e:
                raise DataRunFuncError(
                    'json_loads() fail. response_data is:\n'
                    '{}\n__END_RESPONSE_DATA__'.format(response_data))
        
        if callback is not None:
            callback(response_data)
    
    http_post_request(host, path, data,
            use_https=use_https,
            proxy_host=proxy_host, proxy_port=proxy_port,
            callback=on_response)

def write_debug_last_miniprog(path, func):
    with open(path, mode='w', encoding='utf-8', newline='\n') as fd:
        fd.write(func)

def run_func(core_config, func,
        use_response_json=None, callback=None):
    if core_config.miniprog_host is None:
        raise UserError('\'miniprog_host\' has not been set')
    if core_config.miniprog_path is None:
        raise UserError('\'miniprog_path\' has not been set')
    if core_config.miniprog_proxy_host is not None and \
            core_config.miniprog_proxy_port is None:
        raise UserError('\'miniprog_proxy_port\' has not been set')
    if core_config.auth_secret is None:
        raise UserError('\'auth_secret\' has not been set')
    
    hash_hex = \
            gen_hash(core_config.auth_secret, core_config.miniprog_host) \
            .hexdigest()
    
    if core_config.debug_last_miniprog is not None:
        write_debug_last_miniprog(core_config.debug_last_miniprog, func)
    
    run_func_core(
            core_config.miniprog_host,
            core_config.miniprog_path,
            hash_hex,
            func,
            use_https=core_config.miniprog_https,
            proxy_host=core_config.miniprog_proxy_host,
            proxy_port=core_config.miniprog_proxy_port,
            use_response_json=use_response_json,
            callback=callback)
