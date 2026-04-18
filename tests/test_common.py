import unittest
from pathlib import Path
from tempfile import NamedTemporaryFile

from pywhois2.common import (
    build_key_candidates,
    extract_domain,
    is_ipaddress,
    load_data_yaml,
    load_yaml_mapping,
    parse_generic_no_match_response,
    parse_jprs_no_match_response,
)

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


class CommonHelpersTest(unittest.TestCase):
    def test_build_key_candidates(self):
        self.assertEqual(build_key_candidates("co.jp"), ["co.jp", "jp"])
        self.assertEqual(build_key_candidates(""), [])

    def test_extract_domain(self):
        self.assertEqual(extract_domain("https://whois.example.com/"), "whois.example.com")
        self.assertEqual(extract_domain("whois.example.com/"), "whois.example.com")

    def test_is_ipaddress(self):
        self.assertTrue(is_ipaddress("8.8.8.8"))
        self.assertFalse(is_ipaddress("example.com"))

    def test_yaml_loader_preserves_no_key(self):
        yaml_text = """
common:
  server: whois.iana.org
  template:
    - common.tpl
no:
  server: whois.norid.no
  template:
    - no.tpl
"""
        with NamedTemporaryFile("w+", encoding="utf-8") as handle:
            handle.write(yaml_text)
            handle.flush()

            data = load_yaml_mapping(handle.name)
            self.assertIn("no", data)
            self.assertNotIn(False, data)

            loaded = load_data_yaml(handle.name, "no")
            self.assertEqual(loaded["server"], "whois.norid.no")
            self.assertEqual(loaded["template"], ["no.tpl"])

    def test_parse_jprs_no_match_response(self):
        fixture = (FIXTURE_DIR / "jp_no_match.txt").read_text(encoding="utf-8")
        result = parse_jprs_no_match_response(fixture, "osrebibou.jp")

        self.assertEqual(result["domain_name"], "osrebibou.jp")
        self.assertEqual(result["status_text"], "No match!!")
        self.assertTrue(result["available"])

    def test_parse_generic_no_match_response_verisign(self):
        fixture = (FIXTURE_DIR / "com_no_match.txt").read_text(encoding="utf-8")
        result = parse_generic_no_match_response(fixture, "osrebibou123456789.com")

        self.assertEqual(result["domain_name"], "osrebibou123456789.com")
        self.assertEqual(result["status_text"], 'No match for "OSREBIBOU123456789.COM".')
        self.assertTrue(result["available"])

    def test_parse_generic_no_match_response_pir(self):
        fixture = (FIXTURE_DIR / "org_no_match.txt").read_text(encoding="utf-8")
        result = parse_generic_no_match_response(fixture, "osrebibou123456789.org")

        self.assertEqual(result["domain_name"], "osrebibou123456789.org")
        self.assertEqual(result["status_text"], "Domain not found.")
        self.assertTrue(result["available"])

    def test_parse_generic_no_match_response_kr(self):
        fixture = (FIXTURE_DIR / "kr_no_match.txt").read_text(encoding="utf-8")
        result = parse_generic_no_match_response(fixture, "osrebibou123456789.co.kr")

        self.assertEqual(result["domain_name"], "osrebibou123456789.co.kr")
        self.assertEqual(
            result["status_text"],
            "The requested domain was not found in the Registry or Registrar’s WHOIS Server.",
        )
        self.assertTrue(result["available"])

    def test_parse_generic_no_match_response_rdds(self):
        fixture = (FIXTURE_DIR / "ad_no_match.txt").read_text(encoding="utf-8")
        result = parse_generic_no_match_response(fixture, "osrebibou123456789.ad")

        self.assertEqual(result["domain_name"], "osrebibou123456789.ad")
        self.assertEqual(
            result["status_text"],
            "The queried object does not exist: no matching objects found",
        )
        self.assertTrue(result["available"])


if __name__ == "__main__":
    unittest.main()
