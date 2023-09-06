#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Blacknon. All rights reserved.
# Use of this source code is governed by an MIT license
# that can be found in the LICENSE file.
# =======================================================

import json

import argparse
from argparse import RawTextHelpFormatter

from pkg_resources import get_distribution

# from .whois_request import whois_request
from .whois import Whois

# version (setup.pyから取得してくる)
__version__ = get_distribution('pydork').version


def main():
    # parserの作成
    help_text = 'whois parser command.'
    parser = argparse.ArgumentParser(
        description=help_text,
        formatter_class=RawTextHelpFormatter,
    )

    parser.add_argument(
        "target", action="store", type=str, help=""
    )

    # args
    args = parser.parse_args()

    wh = Whois(args.target)
    result = wh.get()

    print(json.dumps(result))

    # whoisを取得してパース処理した結果を出力する
    # hoge = whois_request(args.target, "whois.jprs.jp")
    # print(hoge)


if __name__ == '__main__':
    main()
