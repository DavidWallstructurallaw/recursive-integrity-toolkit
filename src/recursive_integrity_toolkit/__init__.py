"""Expose the package version without importing analytical or optional modules.

Owner IDs:
    Technical Maintainer, PR-016

Future inputs:
    Installed package metadata only.

Future outputs:
    Stable package version and intentionally approved public imports.

Assumptions:
    Importing the root package remains free of file, logging, network, and analysis side effects.

Limits:
    No data loading, configuration, metric, lineage, report, or optional dependency is imported here.

Current phase status:
    Phase 1 package scaffold with version exposure only.
"""

__version__ = "0.1.0.dev2"

__all__ = ["__version__"]
