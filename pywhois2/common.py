import ipaddress
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
