pywhois2
===

Utilities for querying WHOIS servers and parsing results.

Maintenance helpers
---

- Audit TLD and template coverage with `python3 scripts/audit_templates.py`
- Package metadata is managed in `pyproject.toml`
- Run the full CI command locally with `sh .github/scripts/run_ci.sh`
- Build the Docker test image with `docker build -t pywhois2-test .`
