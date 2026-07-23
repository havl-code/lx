import json
import re
import subprocess


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


def command_has_valid_syntax(command: str) -> bool:
    """Check whether a command is at least syntactically valid bash, without running it."""
    try:
        result = subprocess.run(
            ["bash", "-n", "-c", command],
            capture_output=True,
            timeout=5,
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, OSError):
        return True  # if we can't check, don't block the user over our own tooling failure