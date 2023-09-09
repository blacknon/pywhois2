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
Domain Name: {{ domain_name | lower | ORPHRASE }}

Registry Domain ID: {{ registry_domain_id | lower }}
Registry WHOIS Server: {{ registrar_whois_server | lower }}
Creation Date: {{ creation | ORPHRASE }}
Registrar: {{ registrar_name | ORPHRASE }}
Registrar Abuse Contact Email: {{ registrar_email }}
Registrar Abuse Contact Phone: {{ registrar_phone }}

Registry RegistrantID: {{ registrant_id | ORPHRASE }}
RegistrantName: {{ registrant_name | ORPHRASE }}
RegistrantOrganization: {{ registrant_organization | ORPHRASE }}
<group name="registrant_address">
RegistrantStreet: {{ registrant_address | ORPHRASE | joinmatches(" ") }}
RegistrantCity: {{ registrant_address | ORPHRASE | joinmatches(" ") }}
RegistrantState/Province: {{ registrant_address | ORPHRASE | joinmatches(" ") }}
</group>
RegistrantPostal Code: {{ registrant_zip_code | ORPHRASE }}
RegistrantCountry: {{ registrant_country | ORPHRASE }}
RegistrantPhone: {{ registrant_phone | ORPHRASE }}
RegistrantFax: {{ registrant_fax | ORPHRASE }}
RegistrantEmail: {{ registrant_email | ORPHRASE }}

Registry AdminID: {{ admin_id | ORPHRASE }}
AdminName: {{ admin_name | ORPHRASE }}
AdminOrganization: {{ admin_organization | ORPHRASE }}
<group name="admin_address">
AdminStreet: {{ admin_address | ORPHRASE | joinmatches(" ") }}
AdminCity: {{ admin_address | ORPHRASE | joinmatches(" ") }}
AdminState/Province: {{ admin_address | ORPHRASE | joinmatches(" ") }}
</group>
AdminPostal Code: {{ admin_zip_code | ORPHRASE }}
AdminCountry: {{ admin_country | ORPHRASE }}
AdminPhone: {{ admin_phone | ORPHRASE }}
AdminFax: {{ admin_fax | ORPHRASE }}
AdminEmail: {{ admin_email | ORPHRASE }}

Registry TechID: {{ tech_id | ORPHRASE }}
TechName: {{ tech_name | ORPHRASE }}
TechOrganization: {{ tech_organization | ORPHRASE }}
<group name="tech_address">
TechStreet: {{ tech_address | ORPHRASE | joinmatches(" ") }}
TechCity: {{ tech_address | ORPHRASE | joinmatches(" ") }}
TechState/Province: {{ tech_address | ORPHRASE | joinmatches(" ") }}
</group>
TechPostal Code: {{ tech_zip_code | ORPHRASE }}
TechCountry: {{ tech_country | ORPHRASE }}
TechPhone: {{ tech_phone | ORPHRASE }}
TechFax: {{ tech_fax | ORPHRASE }}
TechEmail: {{ tech_email | ORPHRASE }}

Registry BillingID: {{ billing_id | ORPHRASE }}
BillingName: {{ billing_name | ORPHRASE }}
BillingOrganization: {{ billing_organization | ORPHRASE }}
<group name="billing_address">
BillingStreet: {{ billing_address | ORPHRASE | joinmatches(" ") }}
BillingCity: {{ billing_address | ORPHRASE | joinmatches(" ") }}
BillingState/Province: {{ billing_address | ORPHRASE | joinmatches(" ") }}
</group>
BillingPostal Code: {{ billing_zip_code | ORPHRASE }}
BillingCountry: {{ billing_country | ORPHRASE }}
BillingPhone: {{ billing_phone | ORPHRASE }}
BillingFax: {{ billing_fax | ORPHRASE }}
BillingEmail: {{ billing_email | ORPHRASE }}

Name Server: {{ name_servers | ORPHRASE | to_list | joinmatches }}

DNSSEC: {{ dnssec | ORPHRASE }}
</group>
