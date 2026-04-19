import unittest
from pathlib import Path
from unittest.mock import patch

try:
    import ttp  # noqa: F401
except ImportError:  # pragma: no cover
    ttp = None


FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


def load_fixture(name: str) -> str:
    return (FIXTURE_DIR / name).read_text(encoding="utf-8")


class WhoisEndToEndTest(unittest.TestCase):
    def test_generic_no_match_paths(self):
        try:
            from pywhois2.whois import Whois
        except ModuleNotFoundError as exc:  # pragma: no cover
            raise unittest.SkipTest(str(exc))

        cases = [
            ("osrebibou.jp", "jp_no_match.txt", "No match!!"),
            ("osrebibou123456789.com", "com_no_match.txt", 'No match for "OSREBIBOU123456789.COM".'),
            ("osrebibou123456789.org", "org_no_match.txt", "Domain not found."),
            (
                "osrebibou123456789.co.kr",
                "kr_no_match.txt",
                "The requested domain was not found in the Registry or Registrar’s WHOIS Server.",
            ),
            (
                "osrebibou123456789.ad",
                "ad_no_match.txt",
                "The queried object does not exist: no matching objects found",
            ),
        ]

        for domain, fixture_name, status_text in cases:
            with self.subTest(domain=domain), patch(
                "pywhois2.whois.whois_request",
                return_value=load_fixture(fixture_name),
            ):
                result = Whois(domain).get()
                self.assertEqual(result["domain_name"], domain)
                self.assertEqual(result["status_text"], status_text)
                self.assertTrue(result["available"])

    @unittest.skipIf(ttp is None, "ttp is not installed in the current test environment")
    def test_template_backed_domains_parse_end_to_end(self):
        try:
            from pywhois2.whois import Whois
        except ModuleNotFoundError as exc:  # pragma: no cover
            raise unittest.SkipTest(str(exc))

        cases = [
            ("jprs.jp", "jp_whois.txt", "jprs.jp"),
            ("jprs.co.jp", "co_jp_whois.txt", "jprs.co.jp"),
            ("google.com", "google_com_whois.txt", "google.com"),
            ("google.co.kr", "google_co_kr_whois.txt", "google.co.kr"),
            ("nic.uk", "nic_uk_whois.txt", "nic.uk"),
        ]

        for domain, fixture_name, expected in cases:
            with self.subTest(domain=domain), patch(
                "pywhois2.whois.whois_request",
                return_value=load_fixture(fixture_name),
            ):
                result = Whois(domain).get()
                self.assertEqual(result["domain_name"], expected)
                self.assertIn("name_servers", result)
                self.assertTrue(result["name_servers"])
