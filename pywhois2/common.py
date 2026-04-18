import ipaddress
import re
from pathlib import Path
from typing import Any, Dict
from urllib.parse import urlparse
from datetime import date, datetime

import yaml


class _StringKeySafeLoader(yaml.SafeLoader):
    pass


for first_letter, resolvers in list(_StringKeySafeLoader.yaml_implicit_resolvers.items()):
    _StringKeySafeLoader.yaml_implicit_resolvers[first_letter] = [
        resolver for resolver in resolvers
        if resolver[0] != "tag:yaml.org,2002:bool"
    ]


def is_ipaddress(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def build_key_candidates(target_key: str) -> list[str]:
    if not target_key:
        return []

    key_elements = [element for element in target_key.split(".") if element]
    candidates: list[str] = []
    for index in range(len(key_elements)):
        candidates.append(".".join(key_elements[index:]))
    return candidates


def load_yaml_mapping(yaml_path: str) -> Dict[str, Any]:
    yaml_file = Path(yaml_path)
    with yaml_file.open(encoding="utf-8") as file:
        data = yaml.load(file, Loader=_StringKeySafeLoader) or {}

    if not isinstance(data, dict):
        raise TypeError(f"Expected mapping data in {yaml_file}, got {type(data)}")

    return data


def load_data_yaml(yaml_path: str, target_key: str) -> Dict[str, Any]:
    obj = load_yaml_mapping(yaml_path)
    common_data = obj.get("common", {})
    resolved_data: Dict[str, Any] = {}

    for key in build_key_candidates(target_key):
        candidate = obj.get(key)
        if candidate:
            resolved_data = candidate
            break

    return {**common_data, **resolved_data}


def resolve_template_paths(
    templates: list[str] | None,
    template_dir: Path,
    fallback_templates: tuple[str, ...],
) -> tuple[list[Path], list[str]]:
    configured_templates = list(templates or [])
    resolved_paths: list[Path] = []
    missing_templates: list[str] = []

    for template_name in configured_templates:
        template_path = template_dir / template_name
        if template_path.exists():
            if template_path not in resolved_paths:
                resolved_paths.append(template_path)
        else:
            missing_templates.append(template_name)

    if not configured_templates or missing_templates:
        for fallback_name in fallback_templates:
            fallback_path = template_dir / fallback_name
            if fallback_path.exists() and fallback_path not in resolved_paths:
                resolved_paths.append(fallback_path)

    return resolved_paths, missing_templates


def extract_domain(text: str) -> str:
    try:
        parsed = urlparse(text)
    except ValueError:
        return text.rstrip("/")

    if parsed.scheme and parsed.netloc:
        return parsed.netloc.rstrip("/")
    return text.rstrip("/")


def json_serial(obj: Any) -> str:
    if isinstance(obj, (datetime, date)):
        return obj.strftime("%Y/%m/%d %H:%M:%S %z")
    raise TypeError(f"Type {type(obj)} not serializable")


def normalize_result_keys(data: Any) -> Any:
    if isinstance(data, list):
        return [normalize_result_keys(item) for item in data]

    if not isinstance(data, dict):
        return data

    normalized = {key: normalize_result_keys(value) for key, value in data.items()}

    if "created" in normalized and "creation" not in normalized:
        normalized["creation"] = normalized["created"]
    if "creation" in normalized and "created" not in normalized:
        normalized["created"] = normalized["creation"]

    if "domain_names" in normalized and "domain_name" not in normalized:
        normalized["domain_name"] = normalized["domain_names"]

    return normalized


def parse_nominet_uk_response(text: str) -> Dict[str, Any]:
    if "Domain name:" not in text or "Name servers:" not in text:
        return {}

    result: Dict[str, Any] = {}

    def capture(pattern: str, flags: int = 0) -> str | None:
        match = re.search(pattern, text, flags)
        if not match:
            return None
        return match.group(1).strip()

    domain_name = capture(r"^\s*Domain name:\s*\n\s+(.+)$", re.MULTILINE)
    if domain_name:
        result["domain_name"] = domain_name.lower()

    registrant_name = capture(r"^\s*Registrant:\s*\n\s+(.+)$", re.MULTILINE)
    if registrant_name:
        result["registrant_name"] = registrant_name

    registrant_type = capture(r"^\s*Registrant type:\s*\n\s+(.+)$", re.MULTILINE)
    if registrant_type:
        result["registrant_type"] = registrant_type

    address_block = capture(
        r"^\s*Registrant's address:\s*\n((?:\s+.+\n)+?)\n\s*Registrar:",
        re.MULTILINE,
    )
    if address_block:
        lines = [line.strip() for line in address_block.splitlines() if line.strip()]
        if lines:
            result["registrant_address"] = ", ".join(lines)

    registrar_block = capture(r"^\s*Registrar:\s*\n((?:\s+.+\n)+?)\n\s*Relevant dates:", re.MULTILINE)
    if registrar_block:
        lines = [line.strip() for line in registrar_block.splitlines() if line.strip()]
        if lines:
            result["registrar_name"] = " ".join(lines[0].split())
        for line in lines[1:]:
            if line.startswith("URL:"):
                result["registrar_url"] = line.removeprefix("URL:").strip()

    dates_block = capture(r"^\s*Relevant dates:\s*\n((?:\s+.+\n)+?)\n\s*Registration status:", re.MULTILINE)
    if dates_block:
        for line in (line.strip() for line in dates_block.splitlines()):
            if line.startswith("Registered on:"):
                result["created"] = line.removeprefix("Registered on:").strip()
            elif line.startswith("Expiry date:"):
                result["expiration"] = line.removeprefix("Expiry date:").strip()
            elif line.startswith("Last updated:"):
                result["updated"] = line.removeprefix("Last updated:").strip()

    status_text = capture(r"^\s*Registration status:\s*\n\s+(.+)$", re.MULTILINE)
    if status_text:
        result["status_text"] = status_text

    nameserver_block = capture(r"^\s*Name servers:\s*\n((?:\s+.+\n)+?)\n\s*WHOIS lookup made", re.MULTILINE)
    if nameserver_block:
        name_servers = []
        for line in nameserver_block.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            host = stripped.split()[0].rstrip(".").lower()
            if host:
                name_servers.append(host)
        if name_servers:
            result["name_servers"] = name_servers

    return result


def parse_jprs_no_match_response(text: str, target: str) -> Dict[str, Any]:
    if "No match!!" not in text:
        return {}

    result: Dict[str, Any] = {
        "domain_name": target.lower(),
        "status_text": "No match!!",
        "available": True,
    }

    if "JPRS WHOIS" in text:
        result["parser_note"] = "JPRS no-match response"

    return result


def parse_generic_no_match_response(text: str, target: str) -> Dict[str, Any]:
    patterns = (
        "No match for ",
        "Domain not found.",
        "The requested domain was not found in the Registry or Registrar",
        "The queried object does not exist: no matching objects found",
        "NOT FOUND",
        "No entries found",
        "No Data Found",
    )

    status_text = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if any(pattern in stripped for pattern in patterns):
            status_text = stripped
            break

    if status_text is None and "登録されていません" in text:
        status_text = "Domain is not registered."

    if status_text is None:
        return {}

    return {
        "domain_name": target.lower(),
        "status_text": status_text,
        "available": True,
        "parser_note": "Generic no-match response",
    }
