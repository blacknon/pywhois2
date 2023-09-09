## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Template
## =======================================================

<group>
Domain Name: {{ domain_name | lower | ORPHRASE }}
ROID: {{ domain_roid | ORPHRASE }}
Domain Status: {{ domain_status | ORPHRASE | joinmatches("\n") }}
Registrant: {{ registrant_name | ORPHRASE }}
Registrant Contact Email: {{ registrant_email | ORPHRASE }}
Sponsoring Registrar: {{ registrar_name | ORPHRASE }}
Name Server: {{ name_servers | ORPHRASE | to_list | joinmatches }}
Registration Time: {{ creation | ORPHRASE }}
Expiration Time: {{ expiration | ORPHRASE }}
DNSSEC: {{ dnssec | ORPHRASE }}
</group>
