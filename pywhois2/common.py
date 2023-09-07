#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Blacknon. All rights reserved.
# Use of this source code is governed by an MIT license
# that can be found in the LICENSE file.
# =======================================================

import ipaddress
import yaml


def is_ipaddress(host: str):
    """_summary_

    Args:
        host (str): _description_

    Returns:
        _type_: _description_
    """
    try:
        ipaddress.ip_address(host)
        return True
    except Exception:
        return False


def load_data_yaml(yaml_path: str, target_key: str):
    """

    Args:
        path (str): _description_
    """
    result = {}

    # target_key to  list
    key_candidate = []
    key_elements = target_key.split(".")
    joined_key = ""
    for i in reversed(range(len(key_elements) * -1, 0)):
        if joined_key == "":
            joined_key = key_elements[i]
        else:
            joined_key = "{0}.{1}".format(key_elements[i], joined_key)
        key_candidate.append(joined_key)

    # tld候補のリストを逆順にする
    key_candidate.reverse()

    with open(yaml_path) as file:
        # load data
        obj = yaml.safe_load(file)

        # get common
        common_data = obj.get('common')

        # get key loops
        for k in key_candidate:
            if k in obj:
                res = obj.get(k)
                break

        if len(res) == 0:
            res = common_data

        # server, templateがないdataについてはcommonの内容に上書きさせる
        result = dict(common_data, **res)
        print(result)

        return result
