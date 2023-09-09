## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
def registrant(data):
    if 'registrant' in data:
        extract_data = data['registrant']
        del data['registrant']
        data['registrant_name'] = extract_data['line'][0]
        data['registrant_address'] = extract_data['line'][1]
        data['registrant_address'] += extract_data['line'][2]
        data['registrant_country'] = extract_data['line'][3]

        import sys
        print(data ,file=sys.stderr)
    return data

def admin(data):
    if 'admin' in data:
        extract_data = data['admin']
        del data['admin']
        data['admin_name'] = extract_data['line'][0]
        data['admin_organization'] = extract_data['line'][1]
        data['admin_address'] = extract_data['line'][2]
        data['admin_address'] += extract_data['line'][3]
        data['admin_country'] = extract_data['line'][4]
        data['admin_email'] = extract_data['line'][5]
        data['admin_phone'] = extract_data['line'][6]
        data['admin_fax'] = extract_data['line'][7]
        import sys
        print(data ,file=sys.stderr)
    return data

def tech(data):
    if 'tech' in data:
        extract_data = data['tech']
        del data['tech']
        data['tech_name'] = extract_data['line'][0]
        data['tech_organization'] = extract_data['line'][1]
        data['tech_address'] = extract_data['line'][2]
        data['tech_address'] += extract_data['line'][3]
        data['tech_country'] = extract_data['line'][4]
        data['tech_email'] = extract_data['line'][5]
        data['tech_phone'] = extract_data['line'][6]
        data['tech_fax'] = extract_data['line'][7]

        import sys
        print(data ,file=sys.stderr)
    return data
</macro>

## Template
## =======================================================

<group macro="registrant, admin, tech">
   Domain name: {{ domain_name | lower | ORPHRASE }}
   Registrar:   {{ registrar_id }} ({{ registrar_name | ORPHRASE }})
   Status:      {{ domain_status | lower | ORPHRASE }}

<group name="registrant">
   Registrant:{{ _start_ }}
      {{ line | _line_ | to_list | joinmatches }}
{{ _end_ }}
</group>

<group name="admin">
   Administrative contact:{{ _start_ }}
      {{ line | _line_ | to_list | joinmatches }}
{{ _end_ }}
</group>

<group name="tech">
   Technical contact:{{ _start_ }}
      {{ line | _line_ | to_list | joinmatches }}
{{ _end_ }}
</group>

<group name="name_servers">
   DNS servers:{{ _start_ }}
      {{ name_servers | strip(' ') | ORPHRASE | to_list | joinmatches }}
{{ _end_ }}
</group>

<group name="name_servers">
   DNS servers{{ strip(' ') | ORPHRASE }}:{{ _start_ }}
      {{ name_servers | strip(' ') | ORPHRASE | to_list | joinmatches }}
{{ _end_ }}
</group>

   Registered:    {{ creation | ORPHRASE }}
   Last modified: {{ updated | ORPHRASE }}
   Expires:       {{ expiration | ORPHRASE }}
</group>
