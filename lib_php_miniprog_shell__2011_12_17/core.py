# -*- mode: python; coding: utf-8 -*-
#
# Copyright 2011 Andrej A Antonov <polymorphm@gmail.com>.
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

from .auth import gen_hash
from .main import UserError

def run_func_core(host, path, hash_hex, func):
    # BEGIN TEST STUB ONLY
    print(
        'host: {host!r}\n'
        'path: {path!r}\n'
        'hash_hex: {hash_hex!r}\n\n'
        'func:\n{func}'.format(
            host=host,
            path=path,
            hash_hex=hash_hex,
            func=func,
        ),
    )
    # END TEST STUB ONLY
    
    # TODO: ...

def write_debug_last_miniprog(path, func):
    with open(path, mode='wt', encoding='utf-8', newline='\n') as fd:
        fd.write(func)

def run_func(core_config, func):
    if core_config.miniprog_host is None:
        raise UserError('\'miniprog_host\' has not been set')
    if core_config.miniprog_path is None:
        raise UserError('\'miniprog_path\' has not been set')
    if core_config.auth_secret is None:
        raise UserError('\'auth_secret\' has not been set')
    
    hash_hex = \
            gen_hash(core_config.auth_secret, core_config.miniprog_host) \
            .hexdigest()
    
    if core_config.debug_last_miniprog is not None:
        write_debug_last_miniprog(core_config.debug_last_miniprog, func)
    
    return run_func_core(
            core_config.miniprog_host,
            core_config.miniprog_path,
            hash_hex,
            func)
