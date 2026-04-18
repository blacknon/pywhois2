## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
def dedupe_list_fields(data):
    for key in ('name_servers',):
        if key in data and isinstance(data[key], list):
            deduped = []
            for item in data[key]:
                if item not in deduped:
                    deduped.append(item)
            data[key] = deduped
    return data

def dnssec2only_english(data):
    if 'dnssec' in data and isinstance(data['dnssec'], list):
        data['dnssec'] = data['dnssec'][-1]
    return data

def str2datetime(data):
    import datetime

    tz = datetime.timezone(datetime.timedelta(hours=9))
    for key in ('creation', 'expiration', 'updated'):
        if key in data and isinstance(data[key], str):
            data[key] = datetime.datetime.strptime(
                data[key],
                '%Y. %m. %d.'
            ).replace(tzinfo=tz)
    return data
</macro>


## Template
## =======================================================

<group macro="str2datetime, dnssec2only_english, dedupe_list_fields">
등록인                      : {{ registrant_name_local | ORPHRASE }}
등록인 주소                 : {{ registrant_address_local | ORPHRASE }}
등록인 우편번호             : {{ registrant_zip_code | ORPHRASE }}
책임자                      : {{ admin_name_local | ORPHRASE }}
책임자 전자우편             : {{ admin_email | ORPHRASE }}
책임자 전화번호             : {{ admin_phone | ORPHRASE }}
등록일                      : {{ creation | ORPHRASE }}
최근 정보 변경일            : {{ updated | ORPHRASE }}
사용 종료일                 : {{ expiration | ORPHRASE }}
정보공개여부                : {{ publish_status | ORPHRASE }}
등록대행자                  : {{ registrar_name_local | ORPHRASE }}
DNSSEC                      : {{ dnssec | ORPHRASE | to_list | joinmatches }}

   호스트이름               : {{ name_servers | ORPHRASE | to_list | joinmatches }}

# ENGLISH

Domain Name                 : {{ domain_name }}
Registrant                  : {{ registrant_name | ORPHRASE }}
Registrant Address          : {{ registrant_address | ORPHRASE }}
Registrant Zip Code         : {{ registrant_zip_code | ORPHRASE }}
Administrative Contact(AC)  : {{ admin_name | ORPHRASE }}
AC E-Mail                   : {{ admin_email | ORPHRASE }}
AC Phone Number             : {{ admin_phone | ORPHRASE }}
Registered Date             : {{ creation | ORPHRASE }}
Last Updated Date           : {{ updated | ORPHRASE }}
Expiration Date             : {{ expiration | ORPHRASE }}
Publishes                   : {{ publish_status | ORPHRASE }}
Authorized Agency           : {{ registrar_name | ORPHRASE }}
DNSSEC                      : {{ dnssec | ORPHRASE | to_list | joinmatches }}

   Host Name                : {{ name_servers | ORPHRASE | to_list | joinmatches }}

- KISA/KRNIC WHOIS Service -
</group>
