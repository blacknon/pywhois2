#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Blacknon. All rights reserved.
# Use of this source code is governed by an MIT license
# that can be found in the LICENSE file.
# =======================================================

from pywhois2 import Whois
import json
import datetime


def json_serial(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.strftime("%Y/%m/%d %H:%M:%S %z")
    # 上記以外はサポート対象外.
    raise TypeError("Type %s not serializable" % type(obj))


whois = Whois('unko.co.jp')
result = whois.get()

print(json.dumps(result, default=json_serial))
