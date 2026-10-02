"""Orchestrate local audits, one explicit pair and the packaged Hero example.

Owner IDs:
    PR-013, PR-015, PR-016, PR-018; product orchestration only.
Inputs:
    Explicit CLI declarations, local records and optional local control inputs.
Outputs:
    The accepted safe JSON/Markdown pair, safe diagnostics and declared exits.
Assumptions:
    Each calculated side uses one version and an explicitly declared representation.
Limits:
    No formulas, implicit representation, weighting, content-reference resolution,
    automatic pairs, trajectories or simulation. Lineage requires explicit opt-in. Help and
    version import no analytical dependencies or input/report implementation.
Current phase status:
    Phase 5 Step 8. Accepted kernels own every numerical result.
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
        description="Local integrity audit, explicit version comparison and input validation.")
    parser.add_argument("--version", action="version", version=f"recursive-integrity-toolkit {__version__}")
    commands = parser.add_subparsers(dest="command")
    commands.add_parser("version", help="Show the toolkit version.", allow_abbrev=False)
    example = commands.add_parser("example", help="Extract and audit the packaged local Hero.", allow_abbrev=False)
    example.add_argument("--out", required=True, action=_Once, help="New example workspace; its parent must exist.")
    example.add_argument("--redacted", action=_Once, nargs=0, help="Protect paths and identifiers in reports.")
    example.add_argument("--lineage", action=_Once, nargs=0, help="Calculate ancestry for the packaged Hero target.")
    for command, description in (("audit", "Audit one version or one explicitly declared earlier/later pair."),
                                 ("validate", "Validate inputs without running calculations.")):
        child = commands.add_parser(command, help=description, description=description, allow_abbrev=False)
        child.add_argument("--records", required=True, action=_Once, help="Local records file (CSV, JSONL or Parquet).")
        child.add_argument("--lineage-records", action="append", help="Local ancestor/context records; repeat for multiple files. Audit requires --lineage or config lineage=true.")
        if command == "audit":
            child.add_argument("--lineage", action=_Once, nargs=0, help="Calculate lineage for the primary records using all explicitly loaded records.")
        for flag, help_text in (
            ("provenance", "Local provenance manifest."), ("config", "Local JSON or TOML configuration."),
            ("schema-mapping", "Local declarative schema mapping."), ("version-order", "Local explicit version-order document."),
            ("compare", "One local earlier-version file; --records is the later version."),
            ("state-semantics", "Shared literal state meaning for the explicit pair; requires --compare."),
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
    from .config import load_phase4_invocation, phase4_pair_requested
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
    phase4_pair_requested(options, operation=namespace.command)
    if (namespace.command != "validate" and not options.lineage
            and any(source.role is FileRole.LINEAGE_CONTEXT for source in options.inputs)):
        raise ConfigurationError(ErrorCode.CONFIG_INVALID, "Audit context inputs require explicit lineage execution")
    return options, inventory


def _calculations(bundle, options, *, dataset_versions=None, content_only=False, record_role=None):
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
    versions = bundle.version_order.loaded_versions if dataset_versions is None else dataset_versions
    records = tuple(row for row in bundle.records if record_role is None or row.location.file_role is record_role)
    suffix = "-earlier" if content_only else ""
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

    scope = CalculationScope(versions, tuple(row.record_key for row in records
                             if row.record_key.dataset_version in versions), (),
                             "all_valid_records_in_selected_dataset_scope", "audit-provenance")
    def provenance_result():
        from .io.validation import join_provenance
        if dataset_versions is not None and set(scope.included_record_keys) != {
                row.record_key for row in bundle.records if row.record_key.dataset_version in versions}:
            raise CanonicalValidationError(ErrorCode.SCHEMA_TYPE,
                "Provenance requires one complete version scope; this version spans input roles",
                field="dataset_version")
        joined = bundle.provenance_join if dataset_versions is None else join_provenance(
            bundle.records, bundle.provenance, dataset_versions=versions, strict_mode=options.strict_mode,
            strict_warning_codes=options.configuration.strict_warning_codes)
        return summarize_provenance(joined, scope=scope)
    provenance = None if content_only else attempt(CapabilityKey.PROVENANCE, provenance_result)
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
                return assign_content_states(records, dataset_versions=versions, scope_id="audit-content" + suffix,
                    representation_name=config.name, representation_version=config.version,
                    normalization_profile=config.normalization_profile, content_mode=ContentMode.INLINE)
            exact = attempt(CapabilityKey.CONTENT_DIAGNOSTICS, content)
            if exact is not None:
                represented = exact.representation
                duplicates = None if content_only else attempt(CapabilityKey.CONTENT_DIAGNOSTICS, lambda: detect_exact_duplicates(
                    records, dataset_versions=versions, scope_id="audit-content" + suffix,
                    representation_name=config.name, representation_version=config.version,
                    normalization_profile=config.normalization_profile, content_mode=ContentMode.INLINE))
                if duplicates is not None:
                    results["duplicates"] = duplicates
        else:
            represented = attempt(CapabilityKey.CONTENT_DIAGNOSTICS, lambda: assign_field_states(
                records, dataset_versions=versions, scope_id="audit-representation" + suffix, config=config,
                missing_state_id=options.missing_state_id))
    if represented is not None:
        distribution = attempt(CapabilityKey.CONTENT_DIAGNOSTICS, lambda: calculate_state_distribution(represented))
        if distribution is not None:
            results["distributions"] = (distribution,)
            if options.tail_rule is not None and not content_only:
                tail_options = TailSelectionOptions(options.tail_rule,
                    count_threshold=options.tail_threshold if options.tail_rule == "count_at_or_below" else None,
                    frequency_threshold=options.tail_threshold if options.tail_rule == "frequency_at_or_below" else None)
                tail = attempt(CapabilityKey.CONTENT_DIAGNOSTICS, lambda: select_tail(distribution.unweighted, options=tail_options))
                if tail is not None:
                    results["tail"] = tail
    results["family_errors"] = tuple(failures)
    return results, tuple(exits)


def _pair_calculations(bundle, options):
    """Bind exactly two input roles to single-version results and accepted comparison."""
    from .errors import CanonicalValidationError, ErrorCode
    from .models import CapabilityKey, ExplicitPairContext, FileRole
    from .metrics.diversity import compare_support
    from .reports.assembly import FamilyFailure
    sides = {role: tuple(sorted({row.record_key.dataset_version for row in bundle.records
             if row.location.file_role is role})) for role in (FileRole.RECORDS_PRIMARY, FileRole.RECORDS_COMPARE)}
    earlier, later = sides[FileRole.RECORDS_COMPARE], sides[FileRole.RECORDS_PRIMARY]
    results, exits = _calculations(bundle, options, dataset_versions=later,
        record_role=FileRole.RECORDS_PRIMARY) if len(later) == 1 else ({}, ())
    prior, prior_exits = _calculations(bundle, options, dataset_versions=earlier, content_only=True,
        record_role=FileRole.RECORDS_COMPARE) if len(earlier) == 1 and earlier != later else ({}, ())
    failures = results.get("family_errors", ()) + prior.get("family_errors", ())
    a, b = prior.get("distributions", ()), results.get("distributions", ())
    results["distributions"] = a + b if earlier != later else b
    exits += prior_exits
    try:
        if earlier == later and len(earlier) == 1:
            raise CanonicalValidationError(ErrorCode.VERSION_ORDER_CONFLICT,
                "Comparison requires two distinct versions", field="pair_order")
        if len(earlier) != 1 or len(later) != 1:
            raise CanonicalValidationError(ErrorCode.SCHEMA_TYPE,
                "Each comparison input must contain exactly one version", field="dataset_version")
        if not a or not b:
            raise CanonicalValidationError(ErrorCode.REPRESENTATION_INCOMPATIBLE,
                "Comparison requires a valid declared representation on both sides", field="representation_compatibility")
        first, second = a[0].unweighted, b[0].unweighted
        context = ExplicitPairContext(first.scope, second.scope, first.representation,
                                      second.representation, bundle.version_order)
        results["comparison"] = compare_support(first, second, context=context,
            earlier_state_semantics=options.state_semantics, later_state_semantics=options.state_semantics)
    except Exception as error:
        failures += (FamilyFailure(CapabilityKey.DATASET_LONGITUDINAL, (_message(error),)),)
        exits += (_error_exit(error),)
    results["family_errors"] = failures
    return results, exits


def _primary_versions(bundle):
    """Select the declared primary population without adopting context versions."""
    from .models import FileRole
    return tuple(sorted({row.record_key.dataset_version for row in bundle.records
                         if row.location.file_role is FileRole.RECORDS_PRIMARY}))


def _lineage_calculations(bundle, options):
    """Request graph/root APIs explicitly and retain a bounded family failure."""
    from .errors import CanonicalValidationError, ErrorCode, LineageResourceLimitError
    from .lineage.ancestry import analyze_lineage, SharedAncestryDependence
    from .lineage.graph import LineageLimits
    from .metrics.bounds import lineage_closure_exposure
    from .models import CapabilityKey
    from .reports.assembly import FamilyFailure
    try:
        versions = _primary_versions(bundle)
        if len(versions) > 1:
            raise CanonicalValidationError(ErrorCode.SCHEMA_TYPE,
                "Lineage requires one primary dataset version", field="dataset_version")
        limits = options.configuration.resource_limits
        lineage = analyze_lineage(bundle, target_dataset_version=versions[0] if versions else None,
            limits=LineageLimits(max_nodes=limits.max_lineage_nodes, max_edges=limits.max_lineage_edges,
                max_root_memberships=limits.max_lineage_root_memberships,
                max_root_union_visits=limits.max_lineage_root_union_visits))
        return {"lineage": lineage, "lineage_bounds": lineage_closure_exposure(lineage),
                "shared_ancestry": SharedAncestryDependence(lineage)}, _message_exits(lineage.messages)
    except Exception as error:
        usage = error.resource_usage if isinstance(error, LineageResourceLimitError) else None
        failure = FamilyFailure(CapabilityKey.LINEAGE, (_message(error),), lineage_resource_usage=usage)
        return {"family_errors": (failure,)}, (_error_exit(error),)


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
    input_paths.extend(getattr(namespace, "lineage_records", None) or ())
    try:
        options, config_inventory = _options(namespace)
        input_paths.extend(source.path for source in options.inputs)
        input_paths.extend(entry.path for entry in config_inventory)
        if options.id_salt_file is not None:
            input_paths.append(options.id_salt_file)
        protection = IdentifierProtection.create(secret_file=options.id_salt_file)
        # The input API raises before returning its inventory on invalid order.
        # Capture those bytes before validation and retain them only while the
        # local file identity and metadata remain stable across the attempt.
        from .errors import IngestionError, ErrorCode
        from .models import FileRole
        from .io.loaders import inventory_source
        from .utils.paths import local_input_path
        def order_state(path):
            try:
                info = local_input_path(path).stat()
            except FileNotFoundError:
                raise IngestionError(ErrorCode.FILE_NOT_FOUND, "Version-order input is unavailable",
                    file_role=FileRole.VERSION_ORDER.value) from None
            except OSError:
                raise IngestionError(ErrorCode.FILE_PARSE, "Version-order input cannot be inspected",
                    file_role=FileRole.VERSION_ORDER.value) from None
            return info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns
        order_snapshots = []
        pair_input = any(source.role is FileRole.RECORDS_COMPARE for source in options.inputs)
        if namespace.command != "validate" and (pair_input or options.lineage):
            for source in options.inputs:
                if source.role is FileRole.VERSION_ORDER:
                    state = order_state(source.path)
                    entry = inventory_source(source, limits=options.configuration.resource_limits)
                    if state != order_state(entry.path):
                        raise IngestionError(ErrorCode.FILE_PARSE, "Version-order input changed; retry with a stable file",
                            file_role=FileRole.VERSION_ORDER.value)
                    order_snapshots.append((entry, state))
        order_failure = ()
        try:
            bundle = validate_bundle(AuditBundle(options.inputs), configuration=phase4_validation_configuration(options),
                                     base_directory=Path.cwd())
        except Exception as order_error:
            from .errors import ToolkitError, ErrorCode
            from .models import CapabilityKey, FileRole
            from .reports.assembly import FamilyFailure
            if (not isinstance(order_error, ToolkitError) or order_error.code is not ErrorCode.VERSION_ORDER_CONFLICT
                    or namespace.command == "validate"
                    or not (pair_input or options.lineage)):
                raise
            # Invalid chronology cannot erase independently valid input evidence.
            # Revalidate without an ordering claim; retain the original failure.
            for entry, state in order_snapshots:
                if state != order_state(entry.path):
                    raise IngestionError(ErrorCode.FILE_PARSE, "Version-order input changed; retry with a stable file",
                        file_role=FileRole.VERSION_ORDER.value) from None
            unordered = phase4_validation_configuration(options)
            unordered["version_order"] = []
            bundle = validate_bundle(AuditBundle(tuple(source for source in options.inputs
                if source.role is not FileRole.VERSION_ORDER)), configuration=unordered, base_directory=Path.cwd())
            bundle = replace(bundle, inventory=tuple(sorted(bundle.inventory + tuple(entry for entry, _ in order_snapshots),
                key=lambda entry: (entry.role.value, str(entry.path)))))
            order_failure = tuple(FamilyFailure(family, (_message(order_error),)) for family in (
                *((CapabilityKey.DATASET_LONGITUDINAL,) if pair_input else ()),
                *((CapabilityKey.LINEAGE,) if options.lineage else ())))
        if config_inventory:
            bundle = replace(bundle, inventory=tuple(sorted(bundle.inventory + config_inventory,
                key=lambda entry: (entry.role.value, str(entry.path)))))
        exits = _message_exits(bundle.validation_messages)
        results = {}
        if namespace.command != "validate":
            from .config import phase4_pair_requested
            pair = phase4_pair_requested(options, operation=namespace.command)
            results, calculation_exits = _pair_calculations(bundle, options) if pair else _calculations(
                bundle, options, dataset_versions=_primary_versions(bundle), record_role=FileRole.RECORDS_PRIMARY)
            exits += calculation_exits
            if options.lineage and not order_failure:
                lineage_results, lineage_exits = _lineage_calculations(bundle, options)
                failures = results.get("family_errors", ()) + lineage_results.pop("family_errors", ())
                results.update(lineage_results)
                results["family_errors"] = failures
                exits += lineage_exits
            if order_failure:
                results["family_errors"] = results.get("family_errors", ()) + order_failure
                exits += (1,)
            if not pair and len(_primary_versions(bundle)) > 1:
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


def _example(namespace):
    """Extract fixed local resources into an exclusively created workspace.

    Trusted stable ancestors use the accepted publication path checks. A failed
    extraction removes only identity-matched files created by this invocation.
    Already existing workspaces, including empty directories, are never reused.
    """
    from importlib.resources import files
    import stat
    import sys
    from .utils.paths import (_OUTPUT_CODES, _OutputFailure, _output_local, _output_walk,
        _output_info, _output_recheck, _output_write, _output_clean_stage)
    workspace, root_chain, input_chain, owned = None, None, None, {}
    try:
        workspace = _output_local(namespace.out)
        parent_chain, parent = _output_walk(workspace.parent)
        if not stat.S_ISDIR(parent.st_mode):
            raise _OutputFailure("E_OUTPUT_UNSAFE")
        if _output_info(workspace) is not None:
            raise _OutputFailure("E_OUTPUT_EXISTS")
        names = ("config.json", "records_v1.csv", "records_v2.csv", "provenance.csv",
                 "version_order.json", "EXPECTED_OUTPUTS.md")
        resource = files("recursive_integrity_toolkit").joinpath("data", "hero")
        payloads = {name: resource.joinpath(name).read_bytes() for name in names}
        _output_recheck(parent_chain)
        workspace.mkdir(mode=0o700)
        root_chain, _ = _output_walk(workspace)
        inputs = workspace / "inputs"
        _output_recheck(root_chain)
        inputs.mkdir(mode=0o700)
        input_chain, _ = _output_walk(inputs)
        for name, payload in payloads.items():
            _output_recheck(input_chain)
            _output_write(inputs / name, payload, owned)
        _output_recheck(input_chain)
        invocation = build_parser().parse_args(["audit", "--records", str(inputs / "records_v2.csv"),
            "--compare", str(inputs / "records_v1.csv"), "--config", str(inputs / "config.json"),
            "--provenance", str(inputs / "provenance.csv"), "--version-order", str(inputs / "version_order.json"),
            "--state-semantics", "Hero topic labels retain their literal meaning across v1 and v2.",
            "--out", str(workspace / "reports"), *(["--redacted"] if namespace.redacted else []),
            *(["--lineage"] if namespace.lineage else [])])
        invocation.command = "example"
    except Exception as error:
        cleaned = True
        if input_chain is not None:
            cleaned = _output_clean_stage(workspace / "inputs", input_chain, owned)
        if root_chain is not None:
            try:
                _output_recheck(root_chain)
                workspace.rmdir()
            except Exception:
                cleaned = False
        code = error.code if isinstance(error, _OutputFailure) else "E_OUTPUT_EXISTS" if isinstance(error, FileExistsError) else "E_OUTPUT_IO" if isinstance(error, OSError) else "E_INTERNAL"
        sys.stderr.write(code + ": The example workspace could not be prepared.\n")
        if not cleaned:
            sys.stderr.write("E_OUTPUT_IO: Incomplete example files remain in the selected workspace; inspect it before retrying.\n")
        return _exit_code((_OUTPUT_CODES.get(code, 4), 1 if not cleaned else 0))
    if not namespace.lineage:
        sys.stderr.write("Lineage was not requested. Use rit example --lineage to calculate the Hero ancestry results.\n")
    return _execute(invocation)


def main(argv: Sequence[str] | None = None) -> int:
    """Dispatch supported local work, keeping startup commands import-safe."""
    parser = build_parser()
    try:
        namespace = parser.parse_args(argv)
    except _InvocationError:
        import sys
        sys.stderr.write('E_CONFIG_INVALID: Invalid invocation; use rit audit --help, rit validate --help or rit example --help.\n')
        return 2
    if namespace.command == "version":
        print(f"recursive-integrity-toolkit {__version__}")
        return 0
    if namespace.command is None:
        parser.print_help()
        return 0
    try:
        return _example(namespace) if namespace.command == "example" else _execute(namespace)
    except Exception:
        import sys
        sys.stderr.write("E_INTERNAL: The local command could not initialize; no exception details are emitted.\n")
        return 4
