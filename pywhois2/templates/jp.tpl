## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
def unpack(data):
    while isinstance(data, list) and data:
        data = data[0]

    if 'dns_keys' in data and isinstance(data['dns_keys'], dict):
        extract_data = data['dns_keys']
        del data['dns_keys']
        data['dns_keys'] = [extract_data['dns_keys']]
    return data

def contact_address2parent(data):
    if 'contact_address' in data and isinstance(data['contact_address'], list):
        extract_data = data['contact_address']
        del data['contact_address']
        for d in extract_data:
            if isinstance(d, dict):
                for k in d.keys():
                    data[k] = d[k]
    return data

def standardize_status(data):
    if 'status' in data and isinstance(data['status'], str):
        value = data['status']
        data['status_text'] = value
        data['status'] = {
            'ok': False,
            'hold': False,
            'to_be_suspended': False,
            'suspended': False
        }

        if value == 'Active':
            data['status']['ok'] = True
        elif value == 'Hold':
            data['status']['hold'] = True
        elif value == 'To be suspended':
            data['status']['to_be_suspended'] = True
        elif value == 'Suspended':
            data['status']['suspended'] = True

    return data

def str2datetime(data):
    import datetime

    if 'creation' in data and isinstance(data['creation'], str):
        data['creation'] = datetime.datetime.strptime(
            "{0} {1}".format(data['creation'], "+0900"),
            '%Y/%m/%d %z'
        )

    if 'expiration' in data and isinstance(data['expiration'], str):
        data['expiration'] = datetime.datetime.strptime(
            "{0} {1}".format(data['expiration'], "+0900"),
            '%Y/%m/%d %z'
        )

    if 'updated' in data and isinstance(data['updated'], str):
        data['updated'] = datetime.datetime.strptime(
            data['updated'].replace("JST", "+0900"),
            '%Y/%m/%d %H:%M:%S (%z)'
        )

    return data
</macro>


## Template
## =======================================================

[ JPRS database provides information on network administration. Its use is    ]
[ restricted to network administration purposes. For further information,     ]
[ use 'whois -h whois.jprs.jp help'. To suppress Japanese output, add'/e'     ]
[ at the end of command, e.g. 'whois -h whois.jprs.jp xxx/e'.                 ]

<group macro="contact_address2parent, standardize_status, str2datetime">
Domain Information: [ドメイン情報]
[Domain Name]                   {{ domain_name | lower }}
[Name Server]                   {{ name_servers | ORPHRASE | to_list | joinmatches }}
[登録年月日]                      {{ creation | ORPHRASE }}
[有効期限]                        {{ expiration | ORPHRASE }}
[最終更新]                        {{ updated | ORPHRASE }}
[状態]                           {{ status | ORPHRASE }}
[登録者名]                        {{ registrant_name_local | ORPHRASE }}
[Registrant]                    {{ registrant_name | ORPHRASE }}
<group name="dns_keys">
[Signing Key]                   {{ dns_keys | ORPHRASE | joinmatches("") }}
                                {{ dns_keys | strip(' ') | ORPHRASE | joinmatches("") }}
</group>

Contact Information: [公開連絡窓口]
[名前]                           {{ contact_name_local | ORPHRASE }}
[Name]                          {{ contact_name | ORPHRASE }}
[Email]                         {{ contact_email | ORPHRASE }}
[Web Page]                      {{ contact_web_page | ORPHRASE }}
[郵便番号]                        {{ contact_zip_code | ORPHRASE }}
<group name="contact_address">
[住所]                           {{ contact_address_local | ORPHRASE | joinmatches(" ") }}
                                {{ contact_address_local | strip(' ') | ORPHRASE | joinmatches(" ") }}
</group>
<group name="contact_address">
[Postal Address]                {{ contact_address | ORPHRASE | joinmatches(", ") }}
                                {{ contact_address | strip(' ') | ORPHRASE | joinmatches(", ") }}
</group>
[電話番号]                        {{ contact_phone | ORPHRASE }}
[FAX番号]                        {{ contact_fax | ORPHRASE }}

</group>

<output macro="unpack" />
