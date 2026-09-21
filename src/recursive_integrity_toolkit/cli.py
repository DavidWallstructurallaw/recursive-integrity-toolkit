"""Orchestrate explicit local single-version audits and input-only validation.

Owner IDs:
    PR-013, PR-015, PR-016, PR-018; product orchestration only.
Inputs:
    Explicit CLI declarations, local records and optional local control inputs.
Outputs:
    The accepted safe JSON/Markdown pair, safe diagnostics and declared exits.
Assumptions:
    Calculations use an explicitly declared representation and one input version.
Limits:
    No formulas, implicit representation, weighting, content-reference resolution,
    comparison, packaged example, simulation or Phase 5 graph execution. Help and
    version import no analytical dependencies or input/report implementation.
Current phase status:
    Phase 4 Step 7. Comparison and example remain deferred to Step 8.
"""
from __future__ import annotations

import argparse
from collections.abc import Sequence

from . import __version__


class _InvocationError(ValueError):
    """Parser failure with no echoed argument or source text."""


class _SafeParser(argparse.ArgumentParser):
    def error(self, message):
        raise _InvocationError("Invalid invocation; use rit audit --help or rit validate --help.")


class _Once(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, self.dest, None) is not None:
            parser.error("competing singleton declarations")
        setattr(namespace, self.dest, values if self.nargs != 0 else True)


def build_parser() -> argparse.ArgumentParser:
    """Build import-safe declarations without reading files or executing work."""
    parser = _SafeParser(prog="rit", allow_abbrev=False,
        description="Local single-version integrity audit and input validation.")
    parser.add_argument("--version", action="version", version=f"recursive-integrity-toolkit {__version__}")
    commands = parser.add_subparsers(dest="command")
    commands.add_parser("version", help="Show the toolkit version.", allow_abbrev=False)
    for command, description in (("audit", "Audit one dataset version using explicit declarations."),
                                 ("validate", "Validate inputs without running calculations.")):
        child = commands.add_parser(command, help=description, description=description, allow_abbrev=False)
        child.add_argument("--records", required=True, action=_Once, help="Local records file (CSV, JSONL or Parquet).")
        for flag, help_text in (
            ("provenance", "Local provenance manifest."), ("config", "Local JSON or TOML configuration."),
            ("schema-mapping", "Local declarative schema mapping."), ("version-order", "Local explicit version-order document."),
            ("compare", "Unsupported until Phase 4 Step 8."), ("state-semantics", "Pair declaration; unsupported until Step 8."),
            ("missing-state-id", "Literal ID required only for explicit_missing_state."),
            ("out", "Output directory; default ./rit-report. Existing targets are never overwritten."),
            ("id-salt-file", "Local 32-4096 byte identifier secret, requiring --redacted."),
            ("tail-threshold", "Explicit integer count or finite frequency threshold.")):
            child.add_argument("--" + flag, action=_Once, help=help_text)
        child.add_argument("--redacted", action=_Once, nargs=0, help="Protect paths and identifiers in every output sink.")
        child.add_argument("--strict", action=_Once, nargs=0, help="Promote only configured strict warning codes.")
        child.add_argument("--record-ids", action=_Once, choices=("preserve", "hash", "omit"))
        child.add_argument("--tail-rule", action=_Once,
            choices=("singleton_count", "count_at_or_below", "frequency_at_or_below"))
    return parser


def _exit_code(codes):
    """P4-D06 precedence, independent of encounter order or numeric ordering."""
    return next((code for code in (4, 2, 3, 1) if code in codes), 0)


def _error_exit(error):
    from .errors import ToolkitError, ErrorCode
    if not isinstance(error, ToolkitError):
        return 4
    if error.code is ErrorCode.CONFIG_INVALID:
        return 2
    if error.code in (ErrorCode.PARENT_FORMAT, ErrorCode.PARENT_AMBIGUOUS,
                      ErrorCode.PARENT_FUTURE_VERSION, ErrorCode.LINEAGE_CYCLE):
        return 3
    return 1


def _message(error, *, fatal=False):
    from .errors import ToolkitError
    from .models import FileRole, RecordKey, ValidationMessage, ValidationSeverity
    from .utils.logging import safe_diagnostic, safe_diagnostic_text
    code = error.code.value if isinstance(error, ToolkitError) else "E_INTERNAL"
    if isinstance(error, ToolkitError):
        diagnostic = safe_diagnostic(error)
        key = diagnostic["record_key"]
        return ValidationMessage(code, ValidationSeverity.FATAL if fatal else ValidationSeverity(diagnostic["severity"]),
            safe_diagnostic_text(code), file_role=FileRole(diagnostic["file_role"]) if diagnostic["file_role"] else None,
            field=diagnostic["field"], record_key=RecordKey(key["dataset_version"], key["record_id"]) if key else None,
            row_number=diagnostic["row_number"], line_number=diagnostic["line_number"])
    return ValidationMessage(code, ValidationSeverity.FATAL if fatal else ValidationSeverity.ERROR,
                             safe_diagnostic_text(code))


def _message_exits(messages):
    from .models import ValidationSeverity
    return tuple(2 if item.code == "E_CONFIG_INVALID" else 3 if item.code in (
        "E_PARENT_FORMAT", "E_PARENT_AMBIGUOUS", "E_PARENT_FUTURE_VERSION", "E_LINEAGE_CYCLE") else 1
        for item in messages if item.severity in (ValidationSeverity.ERROR, ValidationSeverity.FATAL))


def _options(namespace):
    from pathlib import Path
    from .config import load_phase4_invocation
    from .errors import ConfigurationError, ErrorCode
    from .models import FileRole
    declarations = {key: value for key, value in vars(namespace).items()
                    if key not in ("command", "config") and value is not None}
    threshold = declarations.get("tail_threshold")
    if threshold is not None:
        try:
            if declarations.get("tail_rule") == "count_at_or_below":
                # Reject decimal/exponent spellings for a declared integer count.
                if not threshold.isascii() or not threshold.isdecimal():
                    raise ValueError
                declarations["tail_threshold"] = int(threshold)
            else:
                declarations["tail_threshold"] = float(threshold)
        except (ValueError, OverflowError):
            raise ConfigurationError(ErrorCode.CONFIG_INVALID, "Invalid tail threshold") from None
    options, inventory = load_phase4_invocation(cli=declarations, config_path=namespace.config,
                                                base_directory=Path.cwd())
    if options.state_semantics is not None or any(source.role is FileRole.RECORDS_COMPARE for source in options.inputs):
        import sys
        sys.stderr.write("E_CONFIG_INVALID: Comparison requires Phase 4 Step 8.\n")
        raise ConfigurationError(ErrorCode.CONFIG_INVALID, "Comparison is deferred to Step 8")
    if namespace.command == "validate" and options.tail_rule is not None:
        raise ConfigurationError(ErrorCode.CONFIG_INVALID, "Input-only validation does not request tail calculations")
    return options, inventory


def _calculations(bundle, options):
    """Call accepted single-family APIs and retain independent successful work."""
    from .errors import CanonicalValidationError, ErrorCode
    from .models import CalculationScope, CapabilityKey, ContentMode, TailSelectionOptions
    from .reports.assembly import FamilyFailure
    from .metrics.provenance import summarize_provenance
    from .metrics.bounds import direct_closure_exposure
    from .metrics.diversity import calculate_state_distribution
    from .metrics.duplicates import detect_exact_duplicates
    from .metrics.tail import select_tail
    from .representations.field import assign_field_states
    from .representations.content_hash import assign_content_states
    results, failures, exits = {}, [], []
    versions = bundle.version_order.loaded_versions
    if len(versions) > 1:
        error = CanonicalValidationError(ErrorCode.SCHEMA_TYPE, "Audit requires one dataset version", field="dataset_version")
        failures.append(FamilyFailure(CapabilityKey.INGESTION, (_message(error),)))
        return {"family_errors": tuple(failures)}, (1,)
    if not versions:
        return results, ()

    def attempt(family, operation):
        try:
            return operation()
        except Exception as error:
            failures.append(FamilyFailure(family, (_message(error),)))
            exits.append(_error_exit(error))
            return None

    scope = CalculationScope(versions, tuple(row.record_key for row in bundle.records), (),
                             "all_valid_records_in_selected_dataset_scope", "audit-provenance")
    provenance = attempt(CapabilityKey.PROVENANCE, lambda: summarize_provenance(bundle.provenance_join, scope=scope))
    if provenance is not None:
        results["provenance"] = provenance
        closure = attempt(CapabilityKey.PROVENANCE, lambda: direct_closure_exposure(provenance))
        if closure is not None:
            results["closure"] = closure
    config = options.configuration.representation
    represented = None
    if config is not None:
        if config.source == "content_hash":
            def content():
                if config.field not in (None, "content") or config.missing_value_policy not in (None, "error"):
                    raise CanonicalValidationError(ErrorCode.CONFIG_INVALID, "Exact content requires its accepted declaration")
                return assign_content_states(bundle.records, dataset_versions=versions, scope_id="audit-content",
                    representation_name=config.name, representation_version=config.version,
                    normalization_profile=config.normalization_profile, content_mode=ContentMode.INLINE)
            exact = attempt(CapabilityKey.CONTENT_DIAGNOSTICS, content)
            if exact is not None:
                represented = exact.representation
                duplicates = attempt(CapabilityKey.CONTENT_DIAGNOSTICS, lambda: detect_exact_duplicates(
                    bundle.records, dataset_versions=versions, scope_id="audit-content",
                    representation_name=config.name, representation_version=config.version,
                    normalization_profile=config.normalization_profile, content_mode=ContentMode.INLINE))
                if duplicates is not None:
                    results["duplicates"] = duplicates
        else:
            represented = attempt(CapabilityKey.CONTENT_DIAGNOSTICS, lambda: assign_field_states(
                bundle.records, dataset_versions=versions, scope_id="audit-representation", config=config,
                missing_state_id=options.missing_state_id))
    if represented is not None:
        distribution = attempt(CapabilityKey.CONTENT_DIAGNOSTICS, lambda: calculate_state_distribution(represented))
        if distribution is not None:
            results["distributions"] = (distribution,)
            if options.tail_rule is not None:
                tail_options = TailSelectionOptions(options.tail_rule,
                    count_threshold=options.tail_threshold if options.tail_rule == "count_at_or_below" else None,
                    frequency_threshold=options.tail_threshold if options.tail_rule == "frequency_at_or_below" else None)
                tail = attempt(CapabilityKey.CONTENT_DIAGNOSTICS, lambda: select_tail(distribution.unweighted, options=tail_options))
                if tail is not None:
                    results["tail"] = tail
    results["family_errors"] = tuple(failures)
    return results, tuple(exits)


def _run_metadata(options, operation, started_at, started_clock, *, status="complete"):
    from datetime import datetime, timezone
    import platform
    import time
    import uuid
    from .reports.assembly import build_run_metadata
    return build_run_metadata(options=options, run_id=str(uuid.uuid4()), operation=operation,
        started_at=started_at, completed_at=datetime.now(timezone.utc).isoformat(),
        duration_seconds=max(0.0, time.perf_counter() - started_clock),
        python_version=platform.python_version(), platform=platform.system(), run_status=status)


def _error_report(error, options, operation, started_at, started_clock):
    from .result import CanonicalReport, SECTION_ORDER
    from .utils.logging import safe_diagnostic_text, safe_remediation
    message = _message(error, fatal=_error_exit(error) == 4)
    payload = {key: {} if index < 8 else [] for index, key in enumerate(SECTION_ORDER)}
    payload["run"] = _run_metadata(options, operation, started_at, started_clock, status="failed")
    payload["errors"] = [{"code": message.code, "severity": message.severity.value,
        "message": safe_diagnostic_text(message.code),
        "file_role": message.file_role.value if message.file_role is not None else None, "field": message.field,
        "record_key": {"dataset_version": message.record_key.dataset_version, "record_id": message.record_key.record_id}
            if message.record_key is not None else None,
        "row_number": message.row_number, "effect_on_run": "failed",
        "effect_on_capabilities": ["ingestion"], "remediation": safe_remediation(message.code)}]
    return CanonicalReport.from_dict(payload)


def _publish(report, options, protection, input_paths, exits):
    import json
    import sys
    from .reports.assembly import privacy_view
    from .utils.paths import publish_reports
    from .utils.logging import emit_publication_diagnostic
    view = privacy_view(report, mode=options.privacy_mode, record_id_mode=options.record_id_mode, protection=protection)
    payload = view.to_dict()
    for family in ("warnings", "errors"):
        for diagnostic in payload[family]:
            sys.stderr.write(json.dumps(diagnostic, ensure_ascii=True, allow_nan=False) + "\n")
    result = publish_reports(view, options.directory, input_paths=tuple(input_paths))
    if result.status == "complete":
        names = list(result.published_files) if options.privacy_mode == "redacted" else [
            str(options.directory / name) for name in result.published_files]
        sys.stdout.write(json.dumps({"reports": names, "paths_relative_to": "selected_output_directory"
            if options.privacy_mode == "redacted" else None}, ensure_ascii=True) + "\n")
    else:
        emit_publication_diagnostic(result, stream=sys.stderr)
    return _exit_code((*exits, result.exit_code))


def _execute(namespace):
    from dataclasses import replace
    from datetime import datetime, timezone
    from pathlib import Path
    import sys
    import time
    from .config import phase4_validation_configuration, resolve_phase4_options
    from .io.validation import validate_bundle
    from .models import AuditBundle
    from .reports.assembly import assemble_report
    from .result import CanonicalReport
    from .utils.hashing import IdentifierProtection
    from .utils.logging import emit_diagnostic
    started_at, started_clock = datetime.now(timezone.utc).isoformat(), time.perf_counter()
    options, protection, exits = None, None, ()
    input_paths = [getattr(namespace, key) for key in (
        "records", "provenance", "compare", "config", "schema_mapping", "version_order", "id_salt_file")
        if getattr(namespace, key, None) is not None]
    try:
        options, config_inventory = _options(namespace)
        input_paths.extend(source.path for source in options.inputs)
        input_paths.extend(entry.path for entry in config_inventory)
        if options.id_salt_file is not None:
            input_paths.append(options.id_salt_file)
        protection = IdentifierProtection.create(secret_file=options.id_salt_file)
        bundle = validate_bundle(AuditBundle(options.inputs), configuration=phase4_validation_configuration(options),
                                 base_directory=Path.cwd())
        if config_inventory:
            bundle = replace(bundle, inventory=tuple(sorted(bundle.inventory + config_inventory,
                key=lambda entry: (entry.role.value, str(entry.path)))))
        exits = _message_exits(bundle.validation_messages)
        results = {}
        if namespace.command == "audit":
            results, calculation_exits = _calculations(bundle, options)
            exits += calculation_exits
            if len(bundle.version_order.loaded_versions) > 1:
                sys.stderr.write("Audit requires one dataset_version; use rit validate to inspect multiple versions.\n")
        report = assemble_report(bundle, run=_run_metadata(options, namespace.command, started_at, started_clock), **results)
        if namespace.command == "validate":
            payload = report.to_dict()
            for section in ("derived_metrics", "proxy_signals", "simulations"):
                payload[section] = {}
            report = CanonicalReport.from_dict(payload)
        return _publish(report, options, protection, input_paths, exits)
    except Exception as error:
        exits += (_error_exit(error),)
        try:
            if options is None:
                # Invalid configuration cannot weaken protection in its error report.
                options = resolve_phase4_options(cli={"out": namespace.out or "./rit-report",
                                                       "redacted": True, "record_ids": "omit"})
            if protection is None:
                protection = IdentifierProtection.create()
            report = _error_report(error, options, namespace.command, started_at, started_clock)
            return _publish(report, options, protection, input_paths, exits)
        except Exception as reporting_error:
            # No exception text, arguments, traceback or unvalidated argv reaches stderr.
            emit_diagnostic(error, stream=sys.stderr, mode="redacted", record_id_mode="omit")
            emit_diagnostic(reporting_error, stream=sys.stderr, mode="redacted", record_id_mode="omit")
            return _exit_code((*exits, _error_exit(reporting_error)))


def main(argv: Sequence[str] | None = None) -> int:
    """Dispatch supported local work, keeping startup commands import-safe."""
    parser = build_parser()
    try:
        namespace = parser.parse_args(argv)
    except _InvocationError:
        import sys
        sys.stderr.write('E_CONFIG_INVALID: Invalid invocation; use rit audit --help or rit validate --help. '
                         'Comparison and example require Phase 4 Step 8.\n')
        return 2
    if namespace.command == "version":
        print(f"recursive-integrity-toolkit {__version__}")
        return 0
    if namespace.command is None:
        parser.print_help()
        return 0
    try:
        return _execute(namespace)
    except Exception:
        import sys
        sys.stderr.write("E_INTERNAL: The local command could not initialize; no exception details are emitted.\n")
        return 4
