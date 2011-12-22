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

import os.path, base64

MINIPROG_DIR = os.path.join(os.path.dirname(__file__), 'miniprog-parts')
MINIPROG_SEP = '\n// {}\n\n'.format('-' * 60)

def arg_value_encode(value):
    if value is None:
        return 'NULL';
    
    if isinstance(value, bool):
        return 'TRUE' if value else 'FALSE'
    
    if isinstance(value, (int, float)):
        return str(value);
    
    if not isinstance(value, (str, bytes)):
        # first: it is will be str-type
        
        value = str(value)
    
    if isinstance(value, str):
        # second: it is will be bytes-type
        
        value = value.encode()
    
    return 'base64_decode(\'{}\')' \
            .format(base64.b64encode(value).decode())

def compile_arg_part(arg_map):
    return 'global arg__ARG_MAP = array(\n{}\n);\n'.format(
        '\n'.join(
            '    \'{}\' => {},'.format(
                arg_name,
                arg_value_encode(arg_map[arg_name]),
            ) for arg_name in arg_map,
        ),
    )

def read_part(part):
    fn = '{}.txt'.format(part)
    path = os.path.join(MINIPROG_DIR, fn)
    
    with open(path, encoding='utf-8', newline='\n') as fd:
        return fd.read()

def compile_miniprog(part_list, use_common=None, arg_map=None, custom_part=None):
    if use_common is None:
        use_common = True
    
    full_list = []
    
    if use_common:
        full_list.append(read_part('common'))
    
    if arg_map is not None:
        full_list.append(compile_arg_part(arg_map))
    
    for part in part_list:
        full_list.append(read_part(part))
    
    if custom_part is not None:
        full_list.append(custom_part)
    
    return MINIPROG_SEP.join(full_list)
