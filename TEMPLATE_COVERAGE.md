# Template Coverage Audit

- Template files: 175
- TLD entries: 266
- Healthy template refs: 260
- Missing template refs: 0
- Server only: 0
- Empty stubs: 6

## Notes

- `.no` is now read safely as the string key `no` instead of being coerced to YAML boolean `False`.
- Missing TLD-specific template files were added so every configured WHOIS server entry now points at real template files.
- Empty TLD stubs also have placeholder template files now, so future server/template definition work can start from an existing file.
- Current IANA-backed WHOIS definitions were added for `.ad`, `.bh`, `.bm`, and `.mc`.
- Additional official WHOIS definitions were added for `.bb`, `.ps`, and `.za`.
- Official registry WHOIS portals were also used to infer host candidates for `.ao`, `.jo`, and `.lc`.
- The official BelizeNIC WHOIS page was used to infer a host candidate for `.bz`.
- The official LK Domain Registry search endpoint was used to infer a host candidate for `.lk`.
- Official registry / registrar portals were used to infer host candidates for `.bd` and `.bt`.
- Another batch of official registry / WHOIS endpoints was added for `.al`, `.ba`, `.bs`, `.cd`, `.cm`, `.gr`, `.kw`, `.pa`, `.ph`, `.py`, and `.sl`.
- A larger batch of IANA-backed or official-registry-backed candidates was added for `.cu`, `.cv`, `.cw`, `.cy`, `.ga`, `.gh`, `.jm`, `.kh`, `.lr`, `.mp`, `.mt`, `.mv`, `.ni`, `.np`, `.nr`, `.pn`, `.sv`, `.va`, `.vi`, `.vn`, and `.zw`.
- IANA-backed definitions were also added for `.aq`, `.bv`, `.kp`, and `.sj`.
- The remaining empty stubs are intentionally left without WHOIS servers because IANA currently shows them as retired, not assigned, or not present in the root zone: `.an`, `.bl`, `.bq`, `.eh`, `.mf`, `.tp`.
- The authoritative audit can be regenerated with `python3 scripts/audit_templates.py`.
