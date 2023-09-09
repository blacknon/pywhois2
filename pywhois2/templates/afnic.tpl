## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================




## Template
## =======================================================

%%
%% This is the AFNIC Whois server.
%%
%% complete date format: YYYY-MM-DDThh:mm:ssZ
%%
%% Rights restricted by copyright.
%% See https://www.afnic.fr/en/domain-names-and-support/everything-there-is-to-know-about-domain-names/find-a-domain-name-or-a-holder-using-whois/
%%
%%

<group>
domain:                        {{ domain_name | lower | ORPHRASE }}
status:                        {{ domain_status | lower | ORPHRASE }}
eppstatus:                     {{ domain_epp_status | lower | ORPHRASE }}
hold:                          {{ domain_hold_status | lower | ORPHRASE }}
holder-c:                      AES329-FRNIC
admin-c:                       GMS163-FRNIC
tech-c:                        I10396-FRNIC
registrar:                     ASCIO TECHNOLOGIES Inc.
Expiry Date:                   2024-02-19T04:09:07Z
created:                       1999-04-22T22:00:00Z
last-update:                   2022-12-27T10:06:40.87561Z
source:                        FRNIC

nserver:                       {{ name_servers | ORPHRASE | to_list | joinmatches }}
source:                        FRNIC

registrar:                     ASCIO TECHNOLOGIES Inc.
address:                       Orestads Boulevard 108, 10. Sal.th
address:                       DK-2300 COPENHAGUE S
country:                       DK
phone:                         +44.2070159328
fax-no:                        +45.33886101
e-mail:                        nicrelations@ascio.com
website:                       http://www.ascio.com
anonymous:                     No
registered:                    2001-01-15T00:00:00Z
source:                        FRNIC

nic-hdl:                       I10396-FRNIC
type:                          ORGANIZATION
contact:                       INDOM
address:                       124-126, rue de Provence
address:                       75008 Paris
country:                       FR
phone:                         +33.176700567
fax-no:                        +33.148016773
e-mail:                        indom@indom.com
registrar:                     ASCIO TECHNOLOGIES Inc.
anonymous:                     NO
obsoleted:                     NO
eppstatus:                     associated
eppstatus:                     active
eligstatus:                    ok
eligsource:                    REGISTRY
eligdate:                      2013-11-01T00:00:00Z
reachstatus:                   ok
reachmedia:                    email
reachsource:                   REGISTRY
reachdate:                     2013-11-01T00:00:00Z
source:                        FRNIC

nic-hdl:                       AES329-FRNIC
type:                          ORGANIZATION
contact:                       ATP EGORA SA
address:                       33, rue Poncelet
address:                       75017 Paris
country:                       FR
phone:                         +33.147380484
fax-no:                        +33.144440181
e-mail:                        smercier@gmsante.fr
registrar:                     ASCIO TECHNOLOGIES Inc.
anonymous:                     NO
obsoleted:                     NO
eppstatus:                     associated
eppstatus:                     active
eligstatus:                    pending
eligsource:                    REGISTRY
reachstatus:                   not identified
source:                        FRNIC

nic-hdl:                       GMS163-FRNIC
type:                          ORGANIZATION
contact:                       GLOBAL MEDIA SANTE
address:                       114, avenue Charles de Gaulle
address:                       92200 Neuilly-sur-Seine
country:                       FR
phone:                         +33.155626991
e-mail:                        smercier@gmsante.fr
registrar:                     ASCIO TECHNOLOGIES Inc.
anonymous:                     NO
obsoleted:                     NO
eppstatus:                     associated
eppstatus:                     active
eligstatus:                    ok
eligdate:                      2012-09-03T00:00:00Z
reachstatus:                   not identified
source:                        FRNIC

</group>
