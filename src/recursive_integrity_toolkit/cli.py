"""Provide the minimal Phase 1 command-line help and version interface.

Owner IDs:
    Product orchestration, PR-013, PR-016

Future inputs:
    Command-line arguments and, in later phases, explicit local audit configuration.

Future outputs:
    Phase 1 help or version text and a process exit status.

Assumptions:
    The CLI remains a thin orchestrator and never owns analytical formulas.

Limits:
    No files are loaded and no metrics, lineage, simulations, or reports are produced.

Current phase status:
    Phase 1 startup scaffold only.
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from . import __version__


def build_parser() -> argparse.ArgumentParser:
    """Create the Phase 1 help and version parser only."""
    parser = argparse.ArgumentParser(
        prog="rit",
        description=(
            "Recursive Integrity Toolkit Phase 1 scaffold. "
            "Analytical audit functionality is not implemented."
        ),
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"recursive-integrity-toolkit {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("version", help="Show the installed package version.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the Phase 1 help or version command without analytical behavior."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "version":
        print(f"recursive-integrity-toolkit {__version__}")
        return 0
    if args.command is None:
        parser.print_help()
        return 0
    parser.error(f"Unsupported Phase 1 command: {args.command}")
    return 2
