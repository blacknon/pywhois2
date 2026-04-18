import datetime
import unittest
from pathlib import Path

try:
    import ttp
except ImportError:  # pragma: no cover
    ttp = None

from pywhois2.common import parse_nominet_uk_response, resolve_template_paths


ROOT_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT_DIR / "pywhois2" / "templates"
FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


def parse_fixture(template_name: str, fixture_name: str) -> dict:
    if ttp is None:
        raise unittest.SkipTest("ttp is not installed in the current test environment")

    template_paths, missing_templates = resolve_template_paths(
        [template_name],
        template_dir=TEMPLATE_DIR,
        fallback_templates=(),
    )
    if missing_templates:
        raise AssertionError(f"Missing template fixture dependency: {missing_templates}")

    template = template_paths[0].read_text(encoding="utf-8").rstrip()
    fixture = (FIXTURE_DIR / fixture_name).read_text(encoding="utf-8")

    parser = ttp.ttp(fixture, template, log_level="ERROR")
    parser.parse()
    result = parser.result(structure="flat_list")
    if not result or not result[0]:
        raise AssertionError(f"Fixture {fixture_name} did not parse with {template_name}")

    return result[0]


class TemplateRegressionTest(unittest.TestCase):
    def test_kr_template_matches_google_co_kr_style_output(self):
        result = parse_fixture("kr.tpl", "google_co_kr_whois.txt")

        self.assertEqual(result["domain_name"], "google.co.kr")
        self.assertEqual(result["registrant_name"], "Google Korea, LLC")
        self.assertEqual(result["registrant_name_local"], "구글코리아유한회사")
        self.assertEqual(result["registrant_address_local"], "서울시 강남구 역삼동 737 강남파이낸스센터 22층")
        self.assertEqual(result["registrar_name"], "Whois Corp.(http://whois.co.kr)")
        self.assertEqual(result["publish_status"], "Y")
        self.assertEqual(result["dnssec"], "unsigned")
        self.assertEqual(
            result["name_servers"],
            ["ns1.google.com", "ns2.google.com", "ns3.google.com", "ns4.google.com"],
        )
        self.assertEqual(
            result["creation"],
            datetime.datetime(1999, 7, 28, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))),
        )

    def test_common_template_normalizes_domain_status_flags(self):
        result = parse_fixture("common.tpl", "google_com_whois.txt")

        self.assertEqual(result["domain_name"], "google.com")
        self.assertEqual(result["registrant_organization"], "Google LLC")
        self.assertEqual(result["registrar_name"], "MarkMonitor, Inc.")
        self.assertEqual(result["dnssec"], "unsigned")
        self.assertTrue(result["status"]["client_update_prohibited"])
        self.assertTrue(result["status"]["server_transfer_prohibited"])
        self.assertTrue(result["status"]["server_delete_prohibited"])
        self.assertEqual(
            sorted(result["name_servers"]),
            ["ns1.google.com", "ns2.google.com", "ns3.google.com", "ns4.google.com"],
        )

    def test_uk_fallback_parser_matches_current_nominet_style_output(self):
        fixture = (FIXTURE_DIR / "nic_uk_whois.txt").read_text(encoding="utf-8")
        result = parse_nominet_uk_response(fixture)

        self.assertEqual(result["domain_name"], "nic.uk")
        self.assertEqual(result["registrant_name"], "Nominet UK")
        self.assertEqual(
            result["registrant_type"],
            "UK Limited Company, (Company number: 3203859)",
        )
        self.assertEqual(
            result["registrant_address"],
            "Minerva House, Edmund Halley Road, Oxford Science Park, Oxford, OX4 4DQ, GB",
        )
        self.assertEqual(
            result["registrar_name"],
            "No registrar listed. This domain is directly registered with Nominet.",
        )
        self.assertEqual(result["created"], "before Aug-1996")
        self.assertEqual(result["updated"], "16-Nov-2004")
        self.assertEqual(result["status_text"], "No registration status listed.")
        self.assertEqual(
            result["name_servers"],
            [
                "dns1.nic.uk",
                "dns2.nic.uk",
                "dns3.nic.uk",
                "dns4.nic.uk",
                "nsa.nic.uk",
                "nsb.nic.uk",
                "nsc.nic.uk",
                "nsd.nic.uk",
            ],
        )


if __name__ == "__main__":
    unittest.main()
