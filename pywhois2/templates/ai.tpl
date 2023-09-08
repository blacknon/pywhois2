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

<group>
Domain Name: {{ domain_name | lower | _line_ | strip('\n') | strip('\r') }}

Registry Domain ID: {{ registry_domain_id | lower }}
Registry WHOIS Server: {{ registrar_whois_server | lower }}
Creation Date: {{ creation | _line_ | strip('\n') | strip('\r') }}
Registrar: {{ registrar_name | _line_ | strip('\n') | strip('\r') }}
Registrar Abuse Contact Email: {{ registrar_email }}
Registrar Abuse Contact Phone: {{ registrar_phone }}

Registry RegistrantID: {{ registrant_id | _line_ | strip('\n') | strip('\r') }}
RegistrantName: {{ registrant_name | _line_ | strip('\n') | strip('\r') }}
RegistrantOrganization: {{ registrant_organization | _line_ | strip('\n') | strip('\r') }}
<group name="registrant_address">
RegistrantStreet: {{ registrant_address | _line_ | strip('\n') | strip('\r') | joinmatches(" ") }}
RegistrantCity: {{ registrant_address | _line_ | strip('\n') | strip('\r') | joinmatches(" ") }}
RegistrantState/Province: {{ registrant_address | _line_ | strip('\n') | strip('\r') | joinmatches(" ") }}
</group>
RegistrantPostal Code: {{ registrant_zip_code | _line_ | strip('\n') | strip('\r') }}
RegistrantCountry: {{ registrant_country | _line_ | strip('\n') | strip('\r') }}
RegistrantPhone: {{ registrant_phone | _line_ | strip('\n') | strip('\r') }}
RegistrantFax: {{ registrant_fax | _line_ | strip('\n') | strip('\r') }}
RegistrantEmail: {{ registrant_email | _line_ | strip('\n') | strip('\r') }}

Registry AdminID: {{ admin_id | _line_ | strip('\n') | strip('\r') }}
AdminName: {{ admin_name | _line_ | strip('\n') | strip('\r') }}
AdminOrganization: {{ admin_organization | _line_ | strip('\n') | strip('\r') }}
<group name="admin_address">
AdminStreet: {{ admin_address | _line_ | strip('\n') | strip('\r') | joinmatches(" ") }}
AdminCity: {{ admin_address | _line_ | strip('\n') | strip('\r') | joinmatches(" ") }}
AdminState/Province: {{ admin_address | _line_ | strip('\n') | strip('\r') | joinmatches(" ") }}
</group>
AdminPostal Code: {{ admin_zip_code | _line_ | strip('\n') | strip('\r') }}
AdminCountry: {{ admin_country | _line_ | strip('\n') | strip('\r') }}
AdminPhone: {{ admin_phone | _line_ | strip('\n') | strip('\r') }}
AdminFax: {{ admin_fax | _line_ | strip('\n') | strip('\r') }}
AdminEmail: {{ admin_email | _line_ | strip('\n') | strip('\r') }}

Registry TechID: {{ tech_id | _line_ | strip('\n') | strip('\r') }}
TechName: {{ tech_name | _line_ | strip('\n') | strip('\r') }}
TechOrganization: {{ tech_organization | _line_ | strip('\n') | strip('\r') }}
<group name="tech_address">
TechStreet: {{ tech_address | _line_ | strip('\n') | strip('\r') | joinmatches(" ") }}
TechCity: {{ tech_address | _line_ | strip('\n') | strip('\r') | joinmatches(" ") }}
TechState/Province: {{ tech_address | _line_ | strip('\n') | strip('\r') | joinmatches(" ") }}
</group>
TechPostal Code: {{ tech_zip_code | _line_ | strip('\n') | strip('\r') }}
TechCountry: {{ tech_country | _line_ | strip('\n') | strip('\r') }}
TechPhone: {{ tech_phone | _line_ | strip('\n') | strip('\r') }}
TechFax: {{ tech_fax | _line_ | strip('\n') | strip('\r') }}
TechEmail: {{ tech_email | _line_ | strip('\n') | strip('\r') }}

Registry BillingID: {{ billing_id | _line_ | strip('\n') | strip('\r') }}
BillingName: {{ billing_name | _line_ | strip('\n') | strip('\r') }}
BillingOrganization: {{ billing_organization | _line_ | strip('\n') | strip('\r') }}
<group name="billing_address">
BillingStreet: {{ billing_address | _line_ | strip('\n') | strip('\r') | joinmatches(" ") }}
BillingCity: {{ billing_address | _line_ | strip('\n') | strip('\r') | joinmatches(" ") }}
BillingState/Province: {{ billing_address | _line_ | strip('\n') | strip('\r') | joinmatches(" ") }}
</group>
BillingPostal Code: {{ billing_zip_code | _line_ | strip('\n') | strip('\r') }}
BillingCountry: {{ billing_country | _line_ | strip('\n') | strip('\r') }}
BillingPhone: {{ billing_phone | _line_ | strip('\n') | strip('\r') }}
BillingFax: {{ billing_fax | _line_ | strip('\n') | strip('\r') }}
BillingEmail: {{ billing_email | _line_ | strip('\n') | strip('\r') }}

Name Server: {{ name_servers | _line_ | strip('\n') | strip('\r') | to_list | joinmatches }}

DNSSEC: {{ dnssec | _line_ | strip('\n') | strip('\r') }}
</group>
