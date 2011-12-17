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

import sys, importlib

COMMAND_LIST = (
    'php-func',
    'ls',
    'cat',
    'rm',
    'mv',
    'cp',
    'ln',
    'readlink',
    'mkdir',
    'rmdir',
    'get',
    'put',
)

class UserError(Exception):
    pass

def get_package_name():
    return '.'.join(__name__.split('.')[:-1])

def import_module(name):
    return importlib.import_module(name, package=get_package_name())

def import_cmd_module(cmd):
    cmd_module_name = '.{}_cmd'.format(cmd.replace('-', '_'))
    
    return import_module(cmd_module_name)

def get_cmd_description(cmd, is_str_only=None):
    if is_str_only is None:
        is_str_only = False
    
    try:
        cmd_module = import_cmd_module(cmd)
    except ImportError:
        return '(Not implemented command or error)'
    
    description = getattr(cmd_module, 'DESCRIPTION', None)
    
    if is_str_only and description is None:
            description = ''
    
    return description

def print_help():
    print(
        'usage: {prog} <command> ...\n\n'
        'commands:\n{cmd_list}\n\n'
        'See \'{prog} <command> --help\' '
        'for more information on a specific command.'.format(
            prog=sys.argv[0],
            cmd_list='\n'.join(
                '    {cmd}   \t{description}'.format(
                    cmd=cmd,
                    description=get_cmd_description(cmd, is_str_only=True),
                )
                for cmd in COMMAND_LIST
            ),
        )
    )

def main():
    try:
        if len(sys.argv) < 2:
            print_help()
            return
        
        cmd = sys.argv[1]
        
        if cmd == 'help' or \
                '.' in cmd or cmd not in COMMAND_LIST:
            print_help()
            return
        
        cmd_module = import_cmd_module(cmd)
        cmd_prog = '{}-{}'.format(sys.argv[0], cmd)
        cmd_argv = (cmd_prog,) + tuple(sys.argv[2:])
        exit_code = cmd_module.main(argv=cmd_argv)
        
        if exit_code:
            return exit_code
    except UserError as e:
        print('{}'.format(e), file=sys.stderr)
