# pywhois2

`pywhois2` is a Python WHOIS library and CLI.
It queries WHOIS servers directly and parses the response with `ttp`-based text templates.

This project is aimed at TLDs whose WHOIS formats differ enough that template-driven parsing is easier to maintain than a single generic parser.

## Features

- Direct WHOIS queries for domains, hosts, and IP addresses
- Template-based parsing under `pywhois2/templates/`
- Support for localized WHOIS output, including `.jp` and related second-level domains
- JSON-friendly CLI output
- Packaged for modern Python and automated GitHub Actions releases

## Current state

The project is usable, but still evolving.

- Some TLDs still rely on generic fallback templates
- Historical or unassigned TLDs are intentionally left without active WHOIS definitions
- WHOIS output formats can change without notice, so templates may need periodic updates

## Installation

Install from PyPI:

```bash
pip install pywhois2
```

Install from a local checkout:

```bash
git clone https://github.com/blacknon/pywhois2
cd pywhois2
pip install .
```

## Command line usage

Query a domain and print compact JSON:

```bash
pywhois2 mynavi.jp
```

Pretty-print the result:

```bash
pywhois2 --pretty mynavi.co.jp
```

Show the installed version:

```bash
pywhois2 --version
```

If the registry returns a clear no-match response, `pywhois2` returns JSON instead of raising an exception:

```bash
$ pywhois2 osrebibou123456789.com
{"domain_name":"osrebibou123456789.com","status_text":"No match for \"OSREBIBOU123456789.COM\".","available":true,"parser_note":"Generic no-match response"}
```

Detailed example:

```bash
$ pywhois2 --pretty mynavi.jp
{
  "contact_zip_code": "100-0003",
  "contact_email": "nic@mynavi.jp",
  "contact_name": "Mynavi Corporation",
  "contact_name_local": "株式会社マイナビ",
  "updated": "2026/03/10 15:02:12 +0900",
  "status": {
    "ok": true,
    "hold": false,
    "to_be_suspended": false,
    "suspended": false
  },
  "expiration": "2027/02/28 00:00:00 +0900",
  "creation": "2007/02/10 00:00:00 +0900",
  "registrant_name": "Mynavi Corporation",
  "registrant_name_local": "株式会社マイナビ",
  "domain_name": "mynavi.jp",
  "name_servers": [
    "ns-884.awsdns-46.net",
    "ns-1231.awsdns-25.org",
    "ns-226.awsdns-28.com",
    "ns-1786.awsdns-31.co.uk"
  ],
  "status_text": "Active",
  "contact_address": "1-1-1, Hitotsubashi, Chiyoda-ku, Tokyo 100-0003",
  "contact_fax": "03-6267-4013",
  "contact_phone": "03-6267-4129",
  "contact_address_local": "東京都千代田区一ツ橋1-1-1 パレスサイドビル6F"
}
```

Another example, from the current parser output for `mynavi.co.jp`:

```json
{
  "updated": "2026/01/01 01:04:06 +0900",
  "connected": "2011/12/01 00:00:00 +0900",
  "creation": "2011/12/01 00:00:00 +0900",
  "status": {
    "ok": true,
    "registered": false,
    "connected": true,
    "user_reserved": false,
    "advance_registered": false,
    "renamed": false,
    "to_be_deleted": false,
    "deleted": false,
    "negotiated": false
  },
  "tech_name": "AT106JP",
  "registrant_name": "MI13396JP",
  "registrant_organization_type": "Corporation",
  "registrant_organization_type_local": "株式会社",
  "registrant_organization": "Mynavi Support Corporation",
  "registrant_organization_local": "株式会社マイナビサポート",
  "registrant_organization_local2": "かぶしきがいしゃまいなびさぽーと",
  "domain_name": "mynavi.co.jp",
  "name_servers": [
    "ns-687.awsdns-21.net",
    "ns-1295.awsdns-33.org",
    "ns-463.awsdns-57.com",
    "ns-1892.awsdns-44.co.uk"
  ],
  "status_text": "Connected (2026/12/31)",
  "created": "2011/12/01 00:00:00 +0900"
}
```

Current parser output for `google.co.kr`:

```json
{
  "registrar_name": "Whois Corp.(http://whois.co.kr)",
  "publish_status": "Y",
  "expiration": "2026/07/28 00:00:00 +0900",
  "updated": "2010/10/04 00:00:00 +0900",
  "creation": "1999/07/28 00:00:00 +0900",
  "admin_phone": "82.25319000",
  "admin_email": "dns-admin@google.com",
  "admin_name": "Domain Administrator",
  "registrant_zip_code": "135984",
  "registrant_address": "22nd Floor Gangnam Finance Center 737, Yeoksam-dong Kangnam-ku Seoul",
  "registrant_name": "Google Korea, LLC",
  "domain_name": "google.co.kr",
  "registrar_name_local": "(주)후이즈(http://whois.co.kr)",
  "admin_name_local": "Domain Administrator",
  "registrant_address_local": "서울시 강남구 역삼동 737 강남파이낸스센터 22층",
  "registrant_name_local": "구글코리아유한회사",
  "dnssec": "unsigned",
  "name_servers": [
    "ns1.google.com",
    "ns2.google.com",
    "ns3.google.com",
    "ns4.google.com"
  ],
  "created": "1999/07/28 00:00:00 +0900"
}
```

## Library usage

```python
import json
import datetime

from pywhois2 import Whois


def json_serial(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.strftime("%Y/%m/%d %H:%M:%S %z")
    raise TypeError("Type %s not serializable" % type(obj))


whois = Whois("mynavi.co.jp")
result = whois.get()

print(json.dumps(result, default=json_serial, ensure_ascii=False, indent=2))
```

## Template-based parsing

Parsing is driven by template files in [pywhois2/templates](./pywhois2/templates).
That makes it easier to add support for new WHOIS formats or refine existing parsers incrementally.
For compatibility with older template output, some parsers expose both `creation` and `created` when the upstream template historically used `created`.

If you want to inspect template coverage:

```bash
python3 scripts/audit_templates.py
```

The current inventory is tracked in [TEMPLATE_COVERAGE.md](./TEMPLATE_COVERAGE.md).

You can also experiment with a raw WHOIS response and a template directly with `ttp`:

```bash
$ ttp -d ./tests/fixtures/jp_whois.txt -t ./pywhois2/templates/jp.tpl -o raw
[{'contact_zip_code': '101-0065', 'contact_email': 'email@jprs.co.jp', 'contact_name': 'Japan Registry Services Co.,Ltd.', 'updated': datetime.datetime(2026, 3, 1, 1, 5, 3, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400))), 'expiration': datetime.datetime(2027, 2, 28, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400))), 'creation': datetime.datetime(2001, 2, 2, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400))), 'registrant_name': 'Japan Registry Services Co.,Ltd.', 'domain_name': 'jprs.jp', 'name_servers': ['ns1.jprs.jp', 'ns2.jprs.jp', 'ns3.jprs.jp', 'ns4.jprs.jp'], 'dns_keys': ['7240 8 2'], 'status_text': 'Active', 'status': {'ok': True, 'hold': False, 'to_be_suspended': False, 'suspended': False}, 'contact_address': 'Tokyo, Chiyoda-ku, Chiyoda First Bldg. East, 3-8-1 Nishi-Kanda, Japan', 'contact_fax': '03-5215-8452', 'contact_phone': '03-5215-8451'}]
```

And for the organizational `.jp` templates:

```bash
$ ttp -d ./tests/fixtures/co_jp_whois.txt -t ./pywhois2/templates/xx.jp.tpl -o raw
[{'updated': datetime.datetime(2026, 2, 1, 1, 2, 4, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400))), 'connected': datetime.datetime(2001, 1, 24, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400))), 'creation': datetime.datetime(2001, 1, 22, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400))), 'status_text': 'Connected (2027/01/31)', 'status': {'ok': True, 'registered': False, 'connected': True, 'user_reserved': False, 'advance_registered': False, 'renamed': False, 'to_be_deleted': False, 'deleted': False, 'negotiated': False}, 'signing_key': '63574 8 2', 'tech_name': 'KI59866JP', 'registrant_name': 'SO42861JP', 'registrant_organization_type': 'Company', 'registrant_organization': 'Japan Registry Services Co.,Ltd.', 'domain_name': 'jprs.co.jp', 'name_servers': ['ns1.jprs.co.jp', 'ns2.jprs.co.jp', 'ns3.jprs.co.jp', 'ns4.jprs.co.jp'], 'lock_status': ['AgentChangeLocked']}]
```

## Development

Run the test suite locally:

```bash
python3 -m unittest discover -s tests -v
```

Run the same command set used by CI:

```bash
sh .github/scripts/run_ci.sh
```

Build the Docker test image:

```bash
docker build -t pywhois2-test .
```
