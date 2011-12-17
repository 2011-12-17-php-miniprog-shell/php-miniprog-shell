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

import time, hmac, hashlib

HASH_FUNC = 'sha256'

def new_hash_obj():
    return hashlib.new(HASH_FUNC)

def gen_hash(secret, msg):
    if isinstance(secret, str):
        secret = secret.encode('utf-8')
    if isinstance(msg, str):
        msg = msg.encode('utf-8')
    
    t = str(int(time.time())).encode('utf-8')
    super_secret = hmac.new(secret, t, new_hash_obj)
    m = hmac.new(
            super_secret.hexdigest().encode('utf-8'),
            msg, new_hash_obj)
    
    return m.hexdigest()
