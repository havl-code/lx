import json
import re


class ResponseParseError(Exception):
    """Raised when the LLM's response can't be parsed into the expected shape."""


REQUIRED_KEYS = {"command", "explanation", "risk"}
VALID_JSON_ESCAPES = set('"\\/bfnrtu')


def _repair_invalid_escapes(text: str) -> str:
    """Double up backslashes that aren't valid JSON escape sequences."""
    def replace(match: re.Match) -> str:
        next_char = match.group(1)
        if next_char in VALID_JSON_ESCAPES:
            return match.group(0)
        return "\\\\" + next_char

    return re.sub(r"\\(.)", replace, text)


def parse_llm_response(raw_response: str) -> dict:
    """Parse the LLM's raw text response into a dict with command, explanation, and risk."""
    repaired = _repair_invalid_escapes(raw_response)
    try:
        data = json.loads(repaired)
    except json.JSONDecodeError as exc:
        raise ResponseParseError(
            "The AI did not return valid JSON. Try rephrasing your task."
        ) from exc

    missing_keys = REQUIRED_KEYS - data.keys()
    if missing_keys:
        raise ResponseParseError(
            f"The AI's response was missing expected fields: {missing_keys}"
        )

    return data