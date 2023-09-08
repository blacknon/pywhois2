## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Template
## =======================================================

<group>
Domain Name:                     {{ domain_name }}
Registrar ID:                    {{ registrar_id | _line_ | strip('\n') | strip('\r') }}
Registrar Name:                  {{ registrar_name | _line_ | strip('\n') | strip('\r') }}
Status:                          {{ domain_status | _line_ | strip('\n') | strip('\r') | joinmatches("\n") }}

Registrant Contact ID:           {{ registrant_id | _line_ | strip('\n') | strip('\r') }}
Registrant Contact Name:         {{ registrant_name | _line_ | strip('\n') | strip('\r') }}
Registrant Contact Email:        {{ registrant_email | _line_ | strip('\n') | strip('\r') }}
Registrant Contact Organisation: {{ registrant_organization | _line_ | strip('\n') | strip('\r') }}

Tech Contact ID:                 {{ tech_id | _line_ | strip('\n') | strip('\r') }}
Tech Contact Name:               {{ tech_name | _line_ | strip('\n') | strip('\r') }}
Tech Contact Email:              {{ tech_email | _line_ | strip('\n') | strip('\r') }}
Tech Contact Organisation:       {{ tech_organization | _line_ | strip('\n') | strip('\r') }}

Name Server:                     {{ name_servers | _line_ | strip('\n') | strip('\r') | to_list | joinmatches }}
</group>
