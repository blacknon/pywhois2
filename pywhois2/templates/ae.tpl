## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Template
## =======================================================

<group>
Domain Name:                     {{ domain_name }}
Registrar ID:                    {{ registrar_id | ORPHRASE }}
Registrar Name:                  {{ registrar_name | ORPHRASE }}
Status:                          {{ domain_status | ORPHRASE | joinmatches("\n") }}

Registrant Contact ID:           {{ registrant_id | ORPHRASE }}
Registrant Contact Name:         {{ registrant_name | ORPHRASE }}
Registrant Contact Email:        {{ registrant_email | ORPHRASE }}
Registrant Contact Organisation: {{ registrant_organization | ORPHRASE }}

Tech Contact ID:                 {{ tech_id | ORPHRASE }}
Tech Contact Name:               {{ tech_name | ORPHRASE }}
Tech Contact Email:              {{ tech_email | ORPHRASE }}
Tech Contact Organisation:       {{ tech_organization | ORPHRASE }}

Name Server:                     {{ name_servers | ORPHRASE | to_list | joinmatches }}
</group>
