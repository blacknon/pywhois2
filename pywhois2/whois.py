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
    is_debug = False

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

    def set_debug(self, is_debug: bool):
        """_summary_

        Args:
            is_debug (bool): _description_
        """
        self.is_debug = is_debug

    def get(self):
        """

        """
        result = {}

        # tldごとのデータを取得
        server = self.data.get('server')
        templates = self.data.get('template')

        while True:
            res = self.__get_data(server, templates)

            if 'registrar_whois_server' in res:
                if res['registrar_whois_server'] == server:
                    result = res
                    break

                server = res['registrar_whois_server'].rstrip("/")
                continue

            else:
                result = res
                break

        return result

    def __get_data(self, server: str, templates: list):
        """

        Args:
            server (str): _description_
            templates (list): _description_

        Returns:
            _type_: _description_
        """

        result = {}

        # whois requestを実行、結果の取得
        res = whois_request(self.target, server)

        for template in templates:
            template_path = os.path.join(TEMPLATE_DIR, template)

            # TODO: whois_serverが含まれる場合、serverと一致しない場合は再度whoisを実行させる処理を追加する(comドメインとか向け？)
            with open(template_path, 'r') as file:
                template = file.read().rstrip()
                file.close()

            parser = ttp.ttp(res, template, log_level="ERROR")
            # parser = ttp.ttp(res, template, log_level="DEBUG")
            parser.parse()
            result = parser.result(structure='flat_list')[0]

            if len(result) > 0:
                break

        return result
