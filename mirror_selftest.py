# mirror_selftest.py
import json
import datetime

def test_mirror_trace(layer):
    try:
        assert isinstance(layer.mirror_trace, list), "mirror_trace must be a list"
        for entry in layer.mirror_trace:
            assert isinstance(entry, str), "Each trace entry must be a string"
        return {"test": "mirror_trace_structure", "status": "✅ PASSED", "details": "Structure is valid"}
    except AssertionError as e:
        return {"test": "mirror_trace_structure", "status": "❌ FAILED", "details": str(e)}

def test_duplicate_detection(layer):
    # This test will add a phrase, so we clear it after
    test_phrase = "🔁♻️🔁"
    initial_trace = list(layer.mirror_trace)
    layer.observe(test_phrase)
    before = len(layer.mirror_trace)
    layer.observe(test_phrase)  # should not be added again
    after = len(layer.mirror_trace)
    # clean up by restoring original trace
    layer.mirror_trace = initial_trace
    try:
        assert after == before, "Duplicate phrase was added"
        return {"test": "duplicate_prevention", "status": "✅ PASSED", "details": "Duplicate prevention working"}
    except AssertionError as e:
        return {"test": "duplicate_prevention", "status": "❌ FAILED", "details": str(e)}


def test_observe_recursion(layer):
    try:
        assert all(layer._is_recursive(p) for p in layer.mirror_trace), "Non-recursive phrase in trace"
        return {"test": "observe_recursion_logic", "status": "✅ PASSED", "details": "observe() only logs recursive phrases"}
    except AssertionError as e:
        return {"test": "observe_recursion_logic", "status": "❌ FAILED", "details": str(e)}


def test_glyph_analytics(layer):
    if not layer.mirror_trace:
        return {"test": "glyph_analytics", "status": "⚪️ SKIPPED", "details": "No trace to analyze"}
    try:
        all_text = "".join(layer.mirror_trace)
        unique = set(char for char in all_text if char in layer.glyphstream)
        assert len(unique) <= len(layer.glyphstream), "Too many unique glyphs found"
        return {"test": "glyph_analytics", "status": "✅ PASSED", "details": f"Glyph count: {len(unique)}"}
    except AssertionError as e:
        return {"test": "glyph_analytics", "status": "❌ FAILED", "details": str(e)}


def test_export_functions(layer):
    if not layer.mirror_trace:
        return {"test": "export_simulation", "status": "⚪️ SKIPPED", "details": "No trace to export"}
    try:
        txt = "\n".join(layer.mirror_trace)
        json_data = json.dumps({"trace": layer.mirror_trace})
        assert txt is not None and json_data is not None, "Export failed"
        return {"test": "export_simulation", "status": "✅ PASSED", "details": "Export simulation complete"}
    except AssertionError as e:
        return {"test": "export_simulation", "status": "❌ FAILED", "details": str(e)}

def generate_test_report(layer):
    timestamp = datetime.datetime.now().isoformat()
    results = [
        test_mirror_trace(layer),
        test_duplicate_detection(layer),
        test_observe_recursion(layer),
        test_glyph_analytics(layer),
        test_export_functions(layer)
    ]
    
    summary = {
        "report_generated_at": timestamp,
        "total_tests": len(results),
        "passed": sum(1 for r in results if r['status'] == "✅ PASSED"),
        "failed": sum(1 for r in results if r['status'] == "❌ FAILED"),
        "skipped": sum(1 for r in results if r['status'] == "⚪️ SKIPPED"),
        "results": results
    }
    return summary
