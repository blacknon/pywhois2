#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Blacknon. All rights reserved.
# Use of this source code is governed by an MIT license
# that can be found in the LICENSE file.
# =======================================================

import os
import ttp

from pathlib import Path
from tld import get_tld

from .whois_request import whois_request
from .common import is_ipaddress, load_data_yaml


# CONST
DATA_DIR = "{0}/data".format(Path(__file__).resolve().parent)
TEMPLATE_DIR = "{0}/templates".format(Path(__file__).resolve().parent)


class Whois:
    target = ""  # whoisでの調査対象文字列
    data = {}  # whoisへのrequest, parseに必要となる情報の取得

    def __init__(self, target: str):
        """

        """
        target_key = ""
        if is_ipaddress(target):
            target_key = "ip_address"
        else:
            target_key = get_tld(
                target, fix_protocol=True,
                fail_silently=True
            )

        # load data file
        self.data = load_data_yaml(
            "{0}/{1}".format(DATA_DIR, "data.yml"), target_key)

        self.target = target

    def get(self):
        """
        """
        server = self.data.get('server')
        template_path = os.path.join(TEMPLATE_DIR, self.data.get('template'))
        with open(template_path, 'r') as file:
            template = file.read().rstrip()

            res = whois_request(self.target, server)

            parser = ttp.ttp(res, template, log_level="ERROR")
            parser.parse()
            result = parser.result()

            file.close()

        # TODO: 全Valueにstrip/不要spaceの圧縮処理を追加

        return result
