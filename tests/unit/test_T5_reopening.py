"""T5 remains deferred to Phase 6B; Step 8 opens only the shared closed core."""
import ast
import inspect


def test_T5_reopening_owner_and_placeholder(owner_checker, repo_root):
    owner_checker("metrics/resampling.py", "T5")
    from recursive_integrity_toolkit.metrics import resampling
    source=(repo_root/"src/recursive_integrity_toolkit/metrics/resampling.py").read_text()
    public={node.name for node in ast.parse(source).body if isinstance(node,ast.FunctionDef) and not node.name.startswith("_")}
    assert public=={"expected_diversity_after_steps","simulate_closed_resampling"}
    for fn in (resampling.expected_diversity_after_steps,resampling.simulate_closed_resampling):
        assert not {"q","r","external_distribution","external_reference","reopening_weight","lambda_"} & set(inspect.signature(fn).parameters)
    for name in ("simulate_reopening","external_reference_loss","reopening","reentry_events"):
        assert not hasattr(resampling,name)
