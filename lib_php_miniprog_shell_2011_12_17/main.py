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

import sys, os.path, importlib, functools, traceback, argparse, configparser
import tornado.ioloop
import tornado.stack_context

COMMAND_LIST = (
    'php-func',
    'pwd',
    'ls',
    'view',
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
DEFAULT_CONFIG_FILENAME = 'php-miniprog-shell.cfg'

class UserError(Exception):
    pass

class CmdError(Exception):
    pass

def get_package_name():
    return '.'.join(__name__.split('.')[:-1])

def import_module(name):
    return importlib.import_module(name, package=get_package_name())

def import_cmd_module(cmd):
    cmd_module_name = '.{}_cmd'.format(cmd.replace('-', '_'))
    
    return import_module(cmd_module_name)

def import_argparse_module(cmd):
    cmd_module_name = '.{}_argparse'.format(cmd.replace('-', '_'))
    
    return import_module(cmd_module_name)

def cmd_add_argument(cmd, subparsers):
    try:
        cmd_module = import_argparse_module(cmd)
    except ImportError:
        cmd_module = None
    
    description = getattr(cmd_module, 'DESCRIPTION', None)
    help = getattr(cmd_module, 'HELP', None)
    add_arguments_func = getattr(cmd_module, 'add_arguments', None)
    
    cmd_parser = subparsers.add_parser(cmd, help=help, description=description)
    cmd_parser.set_defaults(cmd=cmd)
    
    if add_arguments_func is not None:
        add_arguments_func(cmd_parser)
    
    return help

def get_config_path(args):
    config_path = args.config
    
    if config_path is None:
        config_path = os.path.join(
                os.path.dirname(sys.argv[0]),
                DEFAULT_CONFIG_FILENAME)
    
    return config_path

def on_finish(exit_code=None):
    tornado.ioloop.IOLoop.instance().stop()
    
    if exit_code is not None:
        exit(exit_code)

def on_error(e_type, e_value, e_traceback):
    try:
        raise e_value
    except UserError as e:
        print('UserError: {}'.format(e), file=sys.stderr)
        exit(2)
    except CmdError as e:
        print('CmdError: {}'.format(e), file=sys.stderr)
        exit(1)
    except Exception as e:
        traceback.print_exc()
        exit(1)

def main():
    with tornado.stack_context.ExceptionStackContext(on_error):
        parser = argparse.ArgumentParser(
                description='Utility for sending commands to remote php www-site')
        
        parser.add_argument(
                '--config',
                help='Custom path to config ini-file')
        parser.add_argument(
                '--miniprog-host',
                help='Host name (and port) of www-site with miniprog-processor php-file')
        parser.add_argument(
                '--miniprog-path',
                help='Path to miniprog-processor php-file')
        parser.add_argument(
                '--miniprog-tor',
                action='store_true',
                help='Connect via Tor Project network')
        parser.add_argument(
                '--debug-last-miniprog',
                help='Path to local-file for outputting last mini-program')
        subparsers = parser.add_subparsers(title='subcommands')
        
        for cmd in COMMAND_LIST:
            cmd_add_argument(cmd, subparsers)
        
        args = parser.parse_args()
        
        config = configparser.ConfigParser(
                interpolation=configparser.ExtendedInterpolation())
        config.read(get_config_path(args))
        
        cmd = args.cmd
        cmd_module = import_cmd_module(cmd)
        cmd_module.cmd(args, config, callback=on_finish)
    
    io_loop = tornado.ioloop.IOLoop.instance().start()
