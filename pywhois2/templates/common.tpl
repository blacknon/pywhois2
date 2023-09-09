## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
def reseller_address2parent(data):
    if 'reseller_address' in data:
        extract_data = data['reseller_address']
        if type(extract_data) == dict:
            del data['reseller_address']
            data['reseller_address'] = extract_data.get('reseller_address')
    return data

def registrant_address2parent(data):
    if 'registrant_address' in data:
        extract_data = data['registrant_address']
        if type(extract_data) == dict:
            del data['registrant_address']
            data['registrant_address'] = extract_data.get('registrant_address')
    return data

def admin_address2parent(data):
    if 'admin_address' in data:
        extract_data = data['admin_address']
        if type(extract_data) == dict:
            del data['admin_address']
            data['admin_address'] = extract_data.get('admin_address')
    return data

def tech_address2parent(data):
    if 'tech_address' in data:
        extract_data = data['tech_address']
        if type(extract_data) == dict:
            del data['tech_address']
            data['tech_address'] = extract_data.get('tech_address')
    return data
</macro>


## Template
## =======================================================

<group macro="reseller_address2parent, registrant_address2parent, admin_address2parent, tech_address2parent">
Domain Name: {{ domain_name | lower | ORPHRASE }}

Registry Domain ID: {{ registry_domain_id | lower }}
Registrar WHOIS Server: {{ registrar_whois_server | lower }}
Registrar URL: {{ registrar_whois_url | lower }}

Updated Date: {{ updated | ORPHRASE }}
Creation Date: {{ creation | ORPHRASE }}
Registrar Registration Expiration Date: {{ expiration | ORPHRASE }}

Registrar: {{ registrar_name | ORPHRASE }}
Registrar IANA ID: {{ registrar_id }}
Registrar Abuse Contact Email: {{ registrar_email }}
Registrar Abuse Contact Phone: {{ registrar_phone }}

Reseller: {{ reseller_name | ORPHRASE }}
<group name="reseller_address">
Reseller Street Address: {{ reseller_address | ORPHRASE | joinmatches(" ") }}
Reseller Other Address Info: {{ reseller_address | ORPHRASE | joinmatches(" ") }}
</group>
Reseller Country: {{ reseller_company | ORPHRASE | joinmatches(" ") }}
Reseller Phone: {{ reseller_phone | ORPHRASE | joinmatches(" ") }}
Reseller Fax: {{ reseller_fax | ORPHRASE | joinmatches(" ") }}
Reseller Customer Service Email: {{ reseller_email | ORPHRASE | joinmatches(" ") }}

Domain Status: {{ domain_status | ORPHRASE | joinmatches("\n") }}

Registry Registrant ID: {{ registrant_id | ORPHRASE }}
Registrant Name: {{ registrant_name | ORPHRASE }}
Registrant Organization: {{ registrant_organization | ORPHRASE }}
<group name="registrant_address">
Registrant Street: {{ registrant_address | ORPHRASE | joinmatches(" ") }}
Registrant City: {{ registrant_address | ORPHRASE | joinmatches(" ") }}
Registrant State/Province: {{ registrant_address | ORPHRASE | joinmatches(" ") }}
</group>
Registrant Postal Code: {{ registrant_zip_code | ORPHRASE }}
Registrant Country: {{ registrant_country | ORPHRASE }}
Registrant Phone: {{ registrant_phone | ORPHRASE }}
Registrant Phone Ext: {{ registrant_phone_ext | ORPHRASE }}
Registrant Fax: {{ registrant_fax | ORPHRASE }}
Registrant Fax Ext: {{ registrant_fax_ext | ORPHRASE }}
Registrant Email: {{ registrant_email | ORPHRASE }}

Registry Admin ID: {{ admin_id | ORPHRASE }}
Admin Name: {{ admin_name | ORPHRASE }}
Admin Organization: {{ admin_organization | ORPHRASE }}
<group name="admin_address">
Admin Street: {{ admin_address | ORPHRASE | joinmatches(" ") }}
Admin City: {{ admin_address | ORPHRASE | joinmatches(" ") }}
Admin State/Province: {{ admin_address | ORPHRASE | joinmatches(" ") }}
</group>
Admin Postal Code: {{ admin_zip_code | ORPHRASE }}
Admin Country: {{ admin_country | ORPHRASE }}
Admin Phone: {{ admin_phone | ORPHRASE }}
Admin Phone Ext: {{ admin_phone_ext | ORPHRASE }}
Admin Fax: {{ admin_fax | ORPHRASE }}
Admin Fax Ext: {{ admin_fax_ext | ORPHRASE }}
Admin Email: {{ admin_email | ORPHRASE }}

Registry Tech ID: {{ tech_id | ORPHRASE }}
Tech Name: {{ tech_name | ORPHRASE }}
Tech Organization: {{ tech_organization | ORPHRASE }}
<group name="tech_address">
Tech Street: {{ tech_address | ORPHRASE | joinmatches(" ") }}
Tech City: {{ tech_address | ORPHRASE | joinmatches(" ") }}
Tech State/Province: {{ tech_address | ORPHRASE | joinmatches(" ") }}
</group>
Tech Postal Code: {{ tech_zip_code | ORPHRASE }}
Tech Country: {{ tech_country | ORPHRASE }}
Tech Phone: {{ tech_phone | ORPHRASE }}
Tech Phone Ext: {{ tech_phone_ext | ORPHRASE }}
Tech Fax: {{ tech_fax | ORPHRASE }}
Tech Fax Ext: {{ tech_fax_ext | ORPHRASE }}
Tech Email: {{ tech_email | ORPHRASE }}

Registry Billing ID: {{ billing_id | ORPHRASE }}
Billing Name: {{ billing_name | ORPHRASE }}
Billing Organization: {{ billing_organization | ORPHRASE }}
<group name="billing_address">
Billing Street: {{ billing_address | ORPHRASE | joinmatches(" ") }}
Billing City: {{ billing_address | ORPHRASE | joinmatches(" ") }}
Billing State/Province: {{ billing_address | ORPHRASE | joinmatches(" ") }}
</group>
Billing Postal Code: {{ billing_zip_code | ORPHRASE }}
Billing Country: {{ billing_country | ORPHRASE }}
Billing Phone: {{ billing_phone | ORPHRASE }}
Billing Email:  {{ billing_email | ORPHRASE }}

Name Server: {{ name_servers | ORPHRASE | to_list | joinmatches }}
DNSSEC: {{ dnssec | ORPHRASE }}
URL of the ICANN WHOIS Data Problem Reporting System: http://wdprs.internic.net/
</group>
