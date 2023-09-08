## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Template
## =======================================================

<group>
Domain Name: {{ domain_name | lower | _line_ | strip('\n') | strip('\r') }}
ROID: {{ domain_roid | _line_ | strip('\n') | strip('\r') }}
Domain Status: {{ domain_status | _line_ | strip('\n') | strip('\r') | joinmatches("\n") }}
Registrant: {{ registrant_name | _line_ | strip('\n') | strip('\r') }}
Registrant Contact Email: {{ registrant_email | _line_ | strip('\n') | strip('\r') }}
Sponsoring Registrar: {{ registrar_name | _line_ | strip('\n') | strip('\r') }}
Name Server: {{ name_servers | _line_ | strip('\n') | strip('\r') | to_list | joinmatches }}
Registration Time: {{ creation | _line_ | strip('\n') | strip('\r') }}
Expiration Time: {{ expiration | _line_ | strip('\n') | strip('\r') }}
DNSSEC: {{ dnssec | _line_ | strip('\n') | strip('\r') }}
</group>
