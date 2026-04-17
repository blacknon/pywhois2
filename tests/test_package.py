import unittest
from pathlib import Path

import pywhois2
from pywhois2.common import load_yaml_mapping, resolve_template_paths


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT_DIR / "pywhois2" / "data" / "data.yml"
TEMPLATE_DIR = ROOT_DIR / "pywhois2" / "templates"


class PackageTest(unittest.TestCase):
    def test_version_is_available_without_optional_runtime_imports(self):
        self.assertEqual(pywhois2.__version__, "0.1.0")

    def test_whois_attribute_is_lazy(self):
        self.assertTrue(callable(pywhois2.__getattr__))

    def test_each_domain_with_server_has_usable_templates(self):
        data = load_yaml_mapping(str(DATA_FILE))

        for domain, config in data.items():
            if domain == "common":
                continue
            if not isinstance(config, dict) or not config or not config.get("server"):
                continue

            with self.subTest(domain=domain):
                template_paths, missing_templates = resolve_template_paths(
                    config.get("template"),
                    template_dir=TEMPLATE_DIR,
                    fallback_templates=("common_iana.tpl", "common_relay.tpl", "common.tpl"),
                )
                self.assertTrue(
                    config.get("template"),
                    f"{domain} should declare at least one template",
                )
                self.assertEqual(
                    missing_templates,
                    [],
                    f"{domain} should not reference missing template files",
                )
                self.assertTrue(
                    template_paths,
                    f"{domain} should resolve at least one usable template",
                )
                self.assertTrue(
                    all(path.exists() for path in template_paths),
                    f"{domain} resolved a non-existent template path",
                )
                configured = set(config["template"])
                resolved = {path.name for path in template_paths}
                self.assertTrue(
                    configured.issubset(resolved),
                    f"{domain} should resolve all explicitly configured templates",
                )

    def test_empty_domain_stubs_do_not_accidentally_define_templates(self):
        data = load_yaml_mapping(str(DATA_FILE))

        for domain, config in data.items():
            if domain == "common":
                continue

            if isinstance(config, dict) and not config:
                with self.subTest(domain=domain):
                    self.assertFalse(config.get("server"))
                    self.assertFalse(config.get("template"))

    def test_empty_domain_stubs_have_placeholder_templates(self):
        data = load_yaml_mapping(str(DATA_FILE))

        for domain, config in data.items():
            if domain == "common":
                continue

            if not isinstance(config, dict) or not config:
                with self.subTest(domain=domain):
                    self.assertTrue(
                        (TEMPLATE_DIR / f"{domain}.tpl").exists(),
                        f"{domain} should have a placeholder template file",
                    )


if __name__ == "__main__":
    unittest.main()
