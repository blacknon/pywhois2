#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Blacknon. All rights reserved.
# Use of this source code is governed by an MIT license
# that can be found in the LICENSE file.
# =======================================================

import ipaddress
import yaml

from urllib.parse import urlparse
from datetime import date, datetime


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
        res = {}
        for k in key_candidate:
            if k in obj:
                res = obj.get(k)
                break

        if len(res) == 0:
            res = common_data

        # server, templateがないdataについてはcommonの内容に上書きさせる
        result = dict(common_data, **res)

        return result


def extract_domain(text: str):
    result = ""
    is_url = False

    try:
        r = urlparse(text)
        is_url = all([r.scheme, r.netloc])
    except Exception:
        is_url = False

    if is_url:
        parsed_url = urlparse(text)
        result = parsed_url.netloc
    else:
        result = text
        result.rstrip("/")

    return result


def json_serial(obj):
    # 日付型の場合には、文字列に変換します
    if isinstance(obj, (datetime, date)):
        return obj.strftime("%Y/%m/%d %H:%M:%S %z")
        # return obj.isoformat()
    # 上記以外はサポート対象外.
    raise TypeError("Type %s not serializable" % type(obj))
