from pathlib import Path
from typing import Any

import ttp
from tld import get_tld

from .whois_request import whois_request
from .common import extract_domain, is_ipaddress, load_data_yaml, resolve_template_paths


PACKAGE_DIR = Path(__file__).resolve().parent
DATA_FILE = PACKAGE_DIR / "data" / "data.yml"
TEMPLATE_DIR = PACKAGE_DIR / "templates"
COMMON_TEMPLATE_FALLBACKS = (
    "common_iana.tpl",
    "common_relay.tpl",
    "common.tpl",
)


class Whois:
    def __init__(self, target: str):
        self.target = target
        self.is_debug = False
        target_key = ""
        if is_ipaddress(target):
            target_key = "ip_address"
        else:
            resolved_tld = get_tld(
                target, fix_protocol=True,
                fail_silently=True
            )
            target_key = str(resolved_tld or "")

        self.data = load_data_yaml(str(DATA_FILE), target_key)

    def set_debug(self, is_debug: bool) -> None:
        self.is_debug = is_debug

    def get(self) -> dict[str, Any]:
        server = self.data.get("server")
        templates = self.data.get("template") or []

        if not server:
            raise ValueError(f"No WHOIS server configured for target: {self.target}")

        while True:
            res = self.__get_data(server, templates)

            if "registrar_whois_server" in res:
                if res["registrar_whois_server"] == server:
                    return res

                server = res["registrar_whois_server"]
                server = extract_domain(server)
                continue

            return res

    def __get_data(self, server: str, templates: list[str]) -> dict[str, Any]:
        res = whois_request(self.target, server)
        template_paths, missing_templates = resolve_template_paths(
            templates,
            template_dir=TEMPLATE_DIR,
            fallback_templates=COMMON_TEMPLATE_FALLBACKS,
        )

        if not template_paths:
            raise FileNotFoundError(
                "No usable templates found "
                f"(configured={templates}, missing={missing_templates}, target={self.target}, server={server})"
            )

        for template_path in template_paths:
            template = template_path.read_text(encoding="utf-8").rstrip()
            parser = ttp.ttp(res, template, log_level="DEBUG" if self.is_debug else "ERROR")
            parser.parse()
            result = parser.result(structure="flat_list")

            if any(result):
                break
        else:
            raise ValueError(
                "Unable to parse WHOIS response "
                f"for target={self.target} using templates={templates}, "
                f"resolved={[path.name for path in template_paths]}, missing={missing_templates}"
            )

        return result[0]
