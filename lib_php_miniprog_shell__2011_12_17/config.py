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

import sys, os.path, configparser

DEFAULT_CONFIG_FILENAME = 'php-miniprog-shell.cfg'
COMMON_CONFIG_META_MAP = {
    'auth.secret': dict(
        get_config_func=lambda config:
                config.get('auth', 'secret', fallback=None),
    ),
    'miniprog.host': dict(
        add_argument_func=lambda parser: parser.add_argument(
            '--miniprog-host',
            help='host name (and port) of www-site with miniprog-processor php-file',
        ),
        get_arg_func=lambda args: args.miniprog_host,
        get_config_func=lambda config: config.get(
                'miniprog', 'host', fallback=None),
    ),
    'miniprog.path': dict(
        add_argument_func=lambda parser: parser.add_argument(
            '--miniprog-path',
            help='path to miniprog-processor php-file',
        ),
        get_arg_func=lambda args: args.miniprog_path,
        get_config_func=lambda config: config.get(
                'miniprog', 'path', fallback=None),
    ),
    'debug.last_miniprog': dict(
        add_argument_func=lambda parser: parser.add_argument(
            '--debug-last-miniprog',
            help='path to local-file for outputting last mini-program',
        ),
        get_arg_func=lambda args: args.debug_last_miniprog,
        get_config_func=lambda config: config.get(
                'debug', 'last-miniprog', fallback=None),
    ),
}

class Config(object):
    def __init__(self, config_meta_map=None):
        if config_meta_map is None:
            config_meta_map = COMMON_CONFIG_META_MAP
        
        self._map = dict()
        self._config_meta_map = config_meta_map
    
    def add_arguments(self, arg_parser):
        arg_parser.add_argument(
            '--config',
            help='custom path to config ini-file',
        )
        
        for config_name in self._config_meta_map:
            config_meta = self._config_meta_map[config_name]
            add_argument_func = config_meta.get('add_argument_func')
            
            if add_argument_func is not None:
                add_argument_func(arg_parser)
    
    def get_config_path(self, arg_parser_args):
        config_path = arg_parser_args.config
        
        if config_path is None:
            config_path = os.path.join(
                    os.path.dirname(sys.argv[0]),
                    DEFAULT_CONFIG_FILENAME)
        
        return config_path
    
    def read(self, arg_parser_args, config_path=None):
        if config_path is None:
            config_path = self.get_config_path(arg_parser_args)
        
        config_parser = configparser.ConfigParser(
                interpolation=configparser.ExtendedInterpolation())
        config_parser.read(config_path)
        
        for config_name in self._config_meta_map:
            config_meta = self._config_meta_map[config_name]
            get_arg_func = config_meta.get('get_arg_func')
            get_config_func = config_meta.get('get_config_func')
            
            if get_arg_func is not None:
                arg_value = get_arg_func(arg_parser_args)
                
                if arg_value is not None:
                    self._map[config_name] = arg_value
                    
                    continue
            
            if get_config_func is not None:
                config_value = get_config_func(config_parser)
                
                if config_value is not None:
                    self._map[config_name] = config_value
    
    def get(self, name):
        return self._map.get(name)
