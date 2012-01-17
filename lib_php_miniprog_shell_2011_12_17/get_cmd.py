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

import base64, os.path, posixpath
from .core_config import get_core_config
from .miniprog import run_miniprog
from .main import CmdError

class GetCmdError(CmdError):
    pass

def cmd(args, config, callback=None):
    core_config = get_core_config(args, config)
    
    source = args.source
    dest = args.dest
    
    if dest is None:
        dest = '.'
    
    if os.path.isdir(dest):
        dest = os.path.join(dest, posixpath.basename(source))
    
    def on_response(response_data):
        error = response_data.get('error')
        
        if error is not None:
            raise GetCmdError(error)
        
        result = response_data.get('result')
        
        if not isinstance(result, str):
            raise GetCmdError('Invalid result type')
        
        data_b = base64.b64decode(result.encode())
        
        with open(dest, 'wb') as fd:
            fd.write(data_b)
        
        if callback is not None:
            callback()
    
    run_miniprog(
        core_config,
        ['get-cmd'],
        arg_map={
            'source': source,
        },
        callback=on_response
    )
