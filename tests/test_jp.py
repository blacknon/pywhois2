import datetime
import unittest
from pathlib import Path

try:
    import ttp
except ImportError:  # pragma: no cover - exercised only in minimal test envs.
    ttp = None

from pywhois2.common import resolve_template_paths
from pywhois2.whois_request import build_whois_query


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


class JPWhoisTemplateTest(unittest.TestCase):
    def test_jp_template_parses_generic_jp_response(self):
        result = parse_fixture("jp.tpl", "jp_whois.txt")

        self.assertEqual(result["domain_name"], "jprs.jp")
        self.assertEqual(
            [name.lower() for name in result["name_servers"]],
            ["ns1.jprs.jp", "ns2.jprs.jp", "ns3.jprs.jp", "ns4.jprs.jp"],
        )
        self.assertEqual(result["registrant_name"], "Japan Registry Services Co.,Ltd.")
        self.assertEqual(result["contact_name"], "Japan Registry Services Co.,Ltd.")
        self.assertEqual(result["contact_email"], "email@jprs.co.jp")
        self.assertEqual(result["status_text"], "Active")
        self.assertTrue(result["status"]["ok"])
        self.assertEqual(
            result["creation"],
            datetime.datetime(2001, 2, 2, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))),
        )
        self.assertEqual(
            result["expiration"],
            datetime.datetime(2027, 2, 28, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))),
        )
        self.assertEqual(
            result["updated"],
            datetime.datetime(2026, 3, 1, 1, 5, 3, tzinfo=datetime.timezone(datetime.timedelta(hours=9))),
        )

    def test_xx_jp_template_parses_organizational_jp_response(self):
        result = parse_fixture("xx.jp.tpl", "co_jp_whois.txt")

        self.assertEqual(result["domain_name"], "jprs.co.jp")
        self.assertEqual(
            [name.lower() for name in result["name_servers"]],
            ["ns1.jprs.co.jp", "ns2.jprs.co.jp", "ns3.jprs.co.jp", "ns4.jprs.co.jp"],
        )
        self.assertEqual(result["registrant_organization"], "Japan Registry Services Co.,Ltd.")
        self.assertEqual(result["registrant_name"], "SO42861JP")
        self.assertEqual(result["tech_name"], "KI59866JP")
        self.assertEqual(result["registrant_organization_type"], "Company")
        self.assertEqual(result["status_text"], "Connected (2027/01/31)")
        self.assertTrue(result["status"]["ok"])
        self.assertTrue(result["status"]["connected"])
        self.assertEqual(
            result["connected"],
            datetime.datetime(2001, 1, 24, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))),
        )
        self.assertEqual(
            result["creation"],
            datetime.datetime(2001, 1, 22, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))),
        )
        self.assertEqual(
            result["updated"],
            datetime.datetime(2026, 2, 1, 1, 2, 4, tzinfo=datetime.timezone(datetime.timedelta(hours=9))),
        )

    def test_jprs_queries_preserve_raw_target(self):
        self.assertEqual(
            build_whois_query("example.jp", "whois.jprs.jp"),
            b"example.jp\r\n",
        )
        self.assertEqual(
            build_whois_query("example.co.jp/e", "whois.jprs.jp"),
            b"example.co.jp/e\r\n",
        )
        self.assertEqual(
            build_whois_query("example.com", "whois.verisign-grs.com"),
            b"example.com\r\n",
        )


if __name__ == "__main__":
    unittest.main()
