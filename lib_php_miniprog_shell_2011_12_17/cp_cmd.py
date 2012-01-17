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

import base64
from .core_config import get_core_config
from .miniprog import run_miniprog
from .main import CmdError

class CpCmdError(CmdError):
    pass

def cmd(args, config, callback=None):
    core_config = get_core_config(args, config)
    
    source = args.source
    dest = args.dest
    
    def on_response(response_data):
        error = response_data.get('error')
        
        if error is not None:
            raise CpCmdError(error)
        
        if callback is not None:
            callback()
    
    run_miniprog(
        core_config,
        ['cp-cmd'],
        arg_map={
            'source': source,
            'dest': dest,
        },
        callback=on_response
    )
