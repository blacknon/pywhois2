#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Blacknon. All rights reserved.
# Use of this source code is governed by an MIT license
# that can be found in the LICENSE file.
# =======================================================

import socket
import socks
import sys


# NOTE: classでやる意味なくね？？？と思ったのでfunctionにしちゃう
def whois_request(query: str, whois_host: str):
    """whois_request
    Args:
        query (str): _description_
        whois_host (str): _description_

    Returns:
        response (str): _description_
    """
    response = b''

    print(whois_host, file=sys.stderr)  # debug
    s = socks.socksocket(socket.AF_INET)
    s.connect((whois_host, 43))

    s.send(bytes(query, 'utf-8') + b"\r\n")

    # recv returns bytes
    while True:
        d = s.recv(4096)
        response += d
        if not d:
            break

    s.close()

    response = response.decode('utf-8', 'replace')

    return response
