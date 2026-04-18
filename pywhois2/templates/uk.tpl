## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
def unpack(data):
    if isinstance(data, list):
        merged = {}
        for item in data:
            if isinstance(item, dict):
                merged.update(item)
        data = merged

    if 'registrant_address' in data and isinstance(data['registrant_address'], list):
        data['registrant_address'] = ", ".join(data['registrant_address'])

    if 'name_servers' in data and isinstance(data['name_servers'], list):
        cleaned = []
        for item in data['name_servers']:
            if not isinstance(item, str):
                continue
            host = item.split()[0].rstrip('.').lower()
            if host:
                cleaned.append(host)
        data['name_servers'] = cleaned

    return data
</macro>

## Template
## =======================================================

<group name="domain">
    Domain name:
        {{ domain_name }}
</group>

<group name="registrant">
    Registrant:
        {{ registrant_name | ORPHRASE }}
    Registrant type:
        {{ registrant_type | ORPHRASE }}
</group>

<group name="registrant_address">
    Registrant's address:{{ _start_ }}
        {{ registrant_address | ORPHRASE | to_list | joinmatches }}
{{ _end_ }}
</group>

<group name="registrar">
    Registrar:
        {{ registrar_name | ORPHRASE }}
        URL: {{ registrar_url | ORPHRASE }}
</group>

<group name="dates">
    Relevant dates:
        Registered on: {{ created | ORPHRASE }}
        Expiry date:  {{ expiration | ORPHRASE }}
        Last updated:  {{ updated | ORPHRASE }}
</group>

<group name="status">
    Registration status:
        {{ status_text | ORPHRASE }}
</group>

<group name="name_servers">
    Name servers:{{ _start_ }}
        {{ name_servers | ORPHRASE | to_list | joinmatches }}
{{ _end_ }}
</group>

<output macro="unpack" />
