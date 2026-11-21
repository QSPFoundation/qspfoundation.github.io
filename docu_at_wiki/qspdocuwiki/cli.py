from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .config import load_config
from .converter import Converter, ConversionReport
from .errors import ConverterError


def _default_config_path() -> Path:
    return Path(__file__).resolve().parent.parent / "config.toml"


def _print_report(report: ConversionReport, command: str) -> int:
    for warning in report.warnings:
        print(f"warning: {warning}", file=sys.stderr)
    for error in report.errors:
        print(f"error: {error}", file=sys.stderr)
    if command == "convert":
        print(f"Converted {report.converted} page(s); skipped {report.skipped} unchanged page(s).")
    elif not report.errors:
        print("Validation completed.")
    return 1 if report.errors else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="qsp-dokuwiki",
        description="Convert configured QSP Markdown and MDX pages to DokuWiki markup.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=_default_config_path(),
        help="Path to converter TOML configuration (default: docu_at_wiki/config.toml).",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate", help="Validate configured sources and conversion support.")
    subparsers.add_parser("convert", help="Convert changed sources and update the local hash manifest.")
    args = parser.parse_args(argv)

    try:
        config = load_config(args.config)
        converter = Converter(config)
        report = converter.validate() if args.command == "validate" else converter.convert()
    except ConverterError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return _print_report(report, args.command)


if __name__ == "__main__":
    raise SystemExit(main())
