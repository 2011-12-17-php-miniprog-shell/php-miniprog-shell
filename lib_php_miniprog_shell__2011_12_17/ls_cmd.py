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

import sys, argparse

from .config import Config

DESCRIPTION = 'List files and directories inside the specified path'

def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    config = Config()
    parser = argparse.ArgumentParser(
            prog=argv[0],
            description=DESCRIPTION)
    
    config.add_arguments(parser)
    parser.add_argument(
        'path',
        nargs='?',
        help='Path to directory that will be scanned',
    )
    
    parser.add_argument(
        '--one',
        help='List one file per line in simple view',
    )
    
    args = parser.parse_args(args=argv[1:])
    config.read(args)
    
    print(args) # TEST ONLY !!
    print(config._map) # TEST ONLY !!
