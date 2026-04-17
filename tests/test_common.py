import unittest
from tempfile import NamedTemporaryFile

from pywhois2.common import (
    build_key_candidates,
    extract_domain,
    is_ipaddress,
    load_data_yaml,
    load_yaml_mapping,
)


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


if __name__ == "__main__":
    unittest.main()
