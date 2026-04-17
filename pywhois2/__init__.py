import json
import argparse
from argparse import RawTextHelpFormatter
from typing import Optional, Sequence

from ._version import __version__
from .common import json_serial


__all__ = ["Whois", "__version__", "main"]


def build_parser() -> argparse.ArgumentParser:
    help_text = "WHOIS parser command."
    parser = argparse.ArgumentParser(
        description=help_text,
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "target",
        action="store",
        type=str,
        help="Domain, host, or IP address to query.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    from .whois import Whois

    parser = build_parser()
    args = parser.parse_args(argv)
    whois = Whois(args.target)
    result = whois.get()
    dump_kwargs = {"default": json_serial, "ensure_ascii": False}
    if args.pretty:
        dump_kwargs["indent"] = 2

    print(json.dumps(result, **dump_kwargs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


def __getattr__(name: str):
    if name == "Whois":
        from .whois import Whois

        return Whois
    raise AttributeError(name)
