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

DESCRIPTION = 'list files and directories inside the specified path'
HELP = DESCRIPTION

def add_arguments(arg_parser):
    arg_parser.add_argument(
        'path',
        nargs='?',
        help='path to directory that will be scanned',
    )
    arg_parser.add_argument(
        '--one',
        action='store_true',
        help='list one file per line in simple view',
    )
