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

from .core_config import get_core_config
from .miniprog import run_miniprog
from .main import CmdError

class LsCmdError(CmdError):
    pass

def cmd(args, config, callback=None):
    core_config = get_core_config(args, config)
    
    path = args.path
    
    if path is None:
        path = '.'
    
    one = args.one
    
    if one is None:
        one = False
    
    def on_response(response_data):
        error = response_data.get('error')
        
        if error is not None:
            raise LsCmdError(error)
        
        result = response_data.get('result')
        
        if not isinstance(result, (tuple, list)):
            raise LsCmdError('Invalid result type')
        
        msg_list = []
        
        for meta in result:
            if not isinstance(meta, dict):
                raise LsCmdError('Invalid result type')
            
            file_name = meta.get('name')
            
            if not isinstance(file_name, str):
                raise LsCmdError('Invalid result type')
            
            if not args.one:
                file_type = meta.get('type')
                
                if file_type is not None:
                    if not isinstance(file_type, str):
                        raise LsCmdError('Invalid result type')                
                else:
                    file_type = '???'
                
                file_stat = meta.get('stat')
                
                if file_stat is not None:
                    if not isinstance(file_stat, dict):
                        raise LsCmdError('Invalid result type')
                    
                    file_size = file_stat.get('size')
                    
                    if not isinstance(file_size, int):
                        raise LsCmdError('Invalid result type')
                else:
                    file_size = '???'
                
                msg_list.append('{}\t{}\t{}'.format(file_type, file_size, file_name))
            else:
                msg_list.append(file_name)
        
        print('\n'.join(msg_list))
        
        if callback is not None:
            callback()
    
    run_miniprog(
        core_config,
        ['ls-cmd'],
        arg_map={
            'path': path,
            'one': one,
        },
        callback=on_response
    )
