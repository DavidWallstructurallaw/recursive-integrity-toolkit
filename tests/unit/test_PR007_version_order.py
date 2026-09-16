"""Phase 2 Step 1 configuration-contract tests for PR-007."""

import pytest

from recursive_integrity_toolkit.config import resolve_config
from recursive_integrity_toolkit.errors import ConfigurationError, ErrorCode


def test_PR007_explicit_list_order_is_preserved() -> None:
    config = resolve_config({"version_order": ["v1", "v2", "v3"]})
    assert config.version_order == ("v1", "v2", "v3")


def test_PR007_duplicate_explicit_version_is_invalid() -> None:
    with pytest.raises(ConfigurationError) as exc_info:
        resolve_config({"version_order": ["v1", "v1"]})
    assert exc_info.value.code is ErrorCode.CONFIG_INVALID


def test_PR007_no_filename_or_lexical_inference_in_step1() -> None:
    config = resolve_config({})
    assert config.version_order == ()
