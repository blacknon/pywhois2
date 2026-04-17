#!/usr/bin/env python3

from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from pywhois2.common import load_yaml_mapping


DATA_FILE = ROOT_DIR / "pywhois2" / "data" / "data.yml"
TEMPLATE_DIR = ROOT_DIR / "pywhois2" / "templates"


def main() -> int:
    data = load_yaml_mapping(str(DATA_FILE))
    template_files = {path.name for path in TEMPLATE_DIR.glob("*.tpl")}

    empty_keys: list[str] = []
    server_only_keys: list[str] = []
    missing_template_refs: list[tuple[str, list[str]]] = []
    healthy_template_keys: list[str] = []

    for key, value in data.items():
        if key == "common":
            continue

        if not isinstance(value, dict) or not value:
            empty_keys.append(str(key))
            continue

        server = value.get("server")
        templates = value.get("template") or []

        if server and not templates:
            server_only_keys.append(str(key))
            continue

        if not templates:
            empty_keys.append(str(key))
            continue

        missing = [template for template in templates if template not in template_files]
        if missing:
            missing_template_refs.append((str(key), missing))
        else:
            healthy_template_keys.append(str(key))

    print("# Template Coverage Audit")
    print()
    print(f"- Template files: {len(template_files)}")
    print(f"- TLD entries: {len(data) - 1}")
    print(f"- Healthy template refs: {len(healthy_template_keys)}")
    print(f"- Missing template refs: {len(missing_template_refs)}")
    print(f"- Server only: {len(server_only_keys)}")
    print(f"- Empty stubs: {len(empty_keys)}")

    print()
    print("## Missing template references")
    for key, missing in missing_template_refs:
        print(f"- {key}: {', '.join(missing)}")

    print()
    print("## Server without template")
    for key in server_only_keys:
        print(f"- {key}")

    print()
    print("## Empty stubs")
    for key in empty_keys:
        print(f"- {key}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
