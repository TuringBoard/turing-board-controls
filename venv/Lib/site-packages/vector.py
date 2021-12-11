# Copyright (c) 2019 Cvsae
# Distributed under the MIT/X11 software license, see the accompanying
# file license http://www.opensource.org/licenses/mit-license.php.

from iters import *

try:
    xrange
except NameError:
    xrange = range

class Vector(list, Iterable):
  pass
