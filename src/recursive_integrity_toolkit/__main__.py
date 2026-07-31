"""Provide the minimal ``python -m recursive_integrity_toolkit`` startup path.

Owner IDs:
    Technical Maintainer, product orchestration

Future inputs:
    Command-line arguments passed to the approved CLI entrypoint.

Future outputs:
    Future CLI exit status.

Assumptions:
    All analytical work will remain outside this startup shim.

Limits:
    This module only delegates to the Phase 1 help and version CLI when executed as a program.

Current phase status:
    Phase 1 package scaffold with startup validation only.
"""

from .cli import main


if __name__ == "__main__":
    raise SystemExit(main())
