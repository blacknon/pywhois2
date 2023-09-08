## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
def contact_address2parent(data):
    if 'contact_address' in data:
        extract_data = data['contact_address']
        del data['contact_address']
        for d in extract_data:
            for k in d.keys():
                data[k] = d[k]
    return data

def str2datetime(data):
    import datetime

    # 登録年月日
    if 'creation' in data:
        if type(data['creation']) == str:
            data['creation'] = datetime.datetime.strptime(
                "{0} {1}".format(data['creation'], "+0900"),
                '%Y/%m/%d %z'
            )

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                "{0} {1}".format(data['expiration'], "+0900"),
                '%Y/%m/%d %z'
            )

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
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

<group macro="contact_address2parent, str2datetime">
Domain Information: [ドメイン情報]
[Domain Name]                   {{ domain_name | lower }}
[Name Server]                   {{ name_servers | _line_ | strip('\n') | strip('\r') | to_list | joinmatches }}
[登録年月日]                      {{ creation | _line_ | strip('\n') | strip('\r') }}
[有効期限]                        {{ expiration | _line_ | strip('\n') | strip('\r') }}
[最終更新]                        {{ updated | _line_ | strip('\n') | strip('\r') }}
[状態]                           {{ status | _line_ | strip('\n') | strip('\r') }}
[登録者名]                        {{ registrant_name_local | _line_ | strip('\n') | strip('\r') }}
[Registrant]                    {{ registrant_name | _line_ | strip('\n') | strip('\r') }}
[Signing Key]                   {{ signing_key | _line_ | strip('\n') | strip('\r') }}

Contact Information: [公開連絡窓口]
[名前]                           {{ contact_name_local | _line_ | strip('\n') | strip('\r') }}
[Name]                          {{ contact_name | _line_ | strip('\n') | strip('\r') }}
[Email]                         {{ contact_email | _line_ | strip('\n') | strip('\r') }}
[Web Page]                      {{ contact_web_page | _line_ | strip('\n') | strip('\r') }}
[郵便番号]                        {{ contact_zip_code | _line_ | strip('\n') | strip('\r') }}
<group name="contact_address">
[住所]                           {{ contact_address_local | _line_ | strip('\n') | strip('\r') | joinmatches(" ") }}
                                {{ contact_address_local | strip(' ') | _line_ | strip('\n') | strip('\r')  | joinmatches(" ") }}
</group>
<group name="contact_address">
[Postal Address]                {{ contact_address | _line_ | strip('\n') | strip('\r') | joinmatches(", ") }}
                                {{ contact_address | strip(' ') | _line_ | strip('\n') | strip('\r')  | joinmatches(", ") }}
</group>
[電話番号]                        {{ contact_phone | _line_ | strip('\n') | strip('\r') }}
[FAX番号]                        {{ contact_fax | _line_ | strip('\n') | strip('\r') }}

</group>
