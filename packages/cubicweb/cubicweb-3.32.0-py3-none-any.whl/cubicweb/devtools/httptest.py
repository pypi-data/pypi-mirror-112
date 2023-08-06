# copyright 2003-2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of CubicWeb.
#
# CubicWeb is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# CubicWeb is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with CubicWeb.  If not, see <https://www.gnu.org/licenses/>.
"""this module contains base classes and utilities for integration with running
http server
"""

import random
import socket


def get_available_port(ports_scan):
    """return the first available port from the given ports range

    Try to connect port by looking for refused connection (111) or transport
    endpoint already connected (106) errors

    Raise a RuntimeError if no port can be found

    :type ports_range: list
    :param ports_range: range of ports to test
    :rtype: int

    .. see:: :func:`test.test_support.bind_port`
    """
    ports_scan = list(ports_scan)
    random.shuffle(ports_scan)  # lower the chance of race condition
    for port in ports_scan:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("localhost", port))
        except OSError as err:
            if err.args[0] in (111, 106):
                return port
        finally:
            s.close()
    raise RuntimeError(
        "get_available_port([ports_range]) cannot find an available port"
    )
