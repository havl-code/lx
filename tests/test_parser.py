import pytest

from lx.parser import parse_llm_response, ResponseParseError


def test_parses_valid_json():
    raw = '{"command": "ls -la", "explanation": "Lists files.", "risk": "low"}'
    result = parse_llm_response(raw)
    assert result["command"] == "ls -la"
    assert result["explanation"] == "Lists files."
    assert result["risk"] == "low"


def test_repairs_unescaped_backslash_in_command():
    raw = (
        '{"command": "find . -type f \\( -iname \'*.pdf\' \\)", '
        '"explanation": "Finds PDFs.", "risk": "low"}'
    )
    result = parse_llm_response(raw)
    assert result["command"] == r"find . -type f \( -iname '*.pdf' \)"


def test_raises_on_completely_invalid_json():
    raw = "this is not json at all"
    with pytest.raises(ResponseParseError):
        parse_llm_response(raw)


def test_raises_on_missing_required_key():
    raw = '{"command": "ls -la", "explanation": "Lists files."}'
    with pytest.raises(ResponseParseError):
        parse_llm_response(raw)