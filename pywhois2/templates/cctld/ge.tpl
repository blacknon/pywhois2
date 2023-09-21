## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

## Template
## =======================================================

<group>
   Domain Name: {{ domain_name | lower | ORPHRASE }}
   Creation Date: {{ created }}
   Registry Expiry Date: {{ expiration }}
   Registrar: {{ registrar_name | ORPHRASE }}
   Domain Status: {{ status | lower | ORPHRASE }}
   Registrant: {{ registrant_name | ORPHRASE }}
   Admin Name: {{ admin_name | ORPHRASE }}
   Admin Email: {{ admin_email | ORPHRASE }}
   Tech Name: {{ tech_name | ORPHRASE }}
   Tech Email: {{ tech_email | ORPHRASE }}
   Name Server: {{ name_servers | ORPHRASE | to_list | joinmatches }}
</group>


TERMS OF USE:
The WHOIS service is provided solely for informational purposes.
You are not authorized to access or query our Whois
database through the use of electronic processes that are high-volume and
automated except as reasonably necessary to register domain names or
modify existing registrations; the Data is provided by NIC for
information purposes only, and to assist persons in obtaining information
about or related to a domain name registration record. NIC does not
guarantee its accuracy. By submitting a Whois query, you agree to abide
by the following terms of use: You agree that you may use this Data only
for lawful purposes and that under no circumstances will you use this Data
to: (1) allow, enable, or otherwise support the transmission of mass
unsolicited, commercial advertising or solicitations via e-mail, telephone,
or facsimile; or (2) enable high volume, automated, electronic processes
that apply to NIC (or its computer systems). The compilation,
repackaging, dissemination or other use of this Data is expressly
prohibited without the prior written consent of NIC. You agree not to
use electronic processes that are automated and high-volume to access or
query the Whois database except as reasonably necessary to register
domain names or modify existing registrations. NIC reserves the right
to restrict your access to the Whois database in its sole discretion to ensure
operational stability.  NIC may restrict or terminate your access to the
Whois database for failure to abide by these terms of use. NIC
reserves the right to modify these terms at any time.
