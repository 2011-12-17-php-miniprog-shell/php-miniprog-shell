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

class CoreConfig(object):
    pass

def get_auth_secret(args, config):
    return config.get('auth', 'secret', fallback=None)

def get_miniprog_host(args, config):
    miniprog_host = args.miniprog_host
    if miniprog_host is None:
        miniprog_host = config.get('miniprog', 'host', fallback=None)
    return miniprog_host

def get_miniprog_path(args, config):
    miniprog_path = args.miniprog_path
    if miniprog_path is None:
        miniprog_path = config.get('miniprog', 'path', fallback=None)
    return miniprog_path

def get_debug_last_miniprog(args, config):
    debug_last_miniprog = args.debug_last_miniprog
    if debug_last_miniprog is None:
        debug_last_miniprog = config.get('debug', 'last-miniprog', fallback=None)
    return debug_last_miniprog

def get_core_config(args, config):
    core_config = CoreConfig()
    
    core_config.auth_secret = get_auth_secret(args, config)
    core_config.miniprog_host = get_miniprog_host(args, config)
    core_config.miniprog_path = get_miniprog_path(args, config)
    core_config.debug_last_miniprog = get_debug_last_miniprog(args, config)
    
    return core_config
