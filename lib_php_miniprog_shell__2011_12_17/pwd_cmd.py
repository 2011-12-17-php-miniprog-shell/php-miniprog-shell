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

def cmd(args, config):
    core_config = get_core_config(args, config)
    
    # BEGIN TEST STUB ONLY
    run_miniprog(
        core_config,
        ['pwd_cmd'],
        arg_map = {
            123: 'abc',
            'bcd': 234,
            'bcd.e': 234.56,
            'x': None,
            'xx': True,
            'xy': False,
            'fignya': 'фигня',
            'fignya_b': 'фигня'.encode(),
        },
    )
    # END TEST STUB ONLY
    
    # TODO: ...
