# lx

[![Tests](https://github.com/havl-code/lx/actions/workflows/tests.yml/badge.svg)](https://github.com/havl-code/lx/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)

**lx** turns plain-English task descriptions into ready-to-use Linux commands, powered entirely by a local LLM (via [Ollama](https://ollama.com)), so it's private, free, and works offline. It **never runs anything automatically**: you always stay in control.

```
What would you like to do? find every pdf larger than 50mb
⠋ Thinking...

Command:     find . -type f -name "*.pdf" -size +50M
Explanation: This command recursively searches the current directory and its
             subdirectories for files that match the PDF extension and are
             larger than 50 megabytes.
Risk:        LOW

Copy command to clipboard? [y/N]
```

## Why

I don't want to memorise every Linux command flag, and I don't want an AI agent auto-executing commands on my machine without me reviewing them first. `lx` is a small, focused tool built around one idea: **an LLM is great at generating a command from a description, but a human should always be the one who decides whether to run it.**

## Design decisions

- **100% local, no cloud APIs.** Everything runs through Ollama on your own machine, so nothing is sent anywhere, and there's no API cost.
- **Never auto-executes.** `lx` only displays a command, an explanation, and a risk level. Copying it to your clipboard is the only optional action it takes, and only with explicit confirmation.
- **Structured, reliable output.** The LLM is prompted to return strict JSON (`command`, `explanation`, `risk`). Since small local models don't always follow formatting instructions perfectly, `lx` includes a JSON-repair step (for common escaping mistakes) and automatic retry logic if parsing still fails.
- **Risk labelling.** Every generated command is labelled `low`, `medium`, or `high` risk, and colour-coded in the terminal (green/yellow/red), so dangerous commands are visually distinct before you ever consider running them.
- **Streamed under the hood.** Responses are read from Ollama as a stream of chunks rather than one blocking call, with a live animated status indicator while the model works. The final result is still shown all at once (not word-by-word), since a partially-generated command or JSON fragment isn't meaningful or safe to display mid-stream.
- **Tested and CI-checked.** Core logic (JSON parsing/repair, input validation) has unit tests, run automatically via GitHub Actions on every push.

## Requirements

- Linux (developed and tested on CachyOS/Arch)
- Python 3.11+
- [Ollama](https://ollama.com) installed and running
- A pulled model (developed against `gemma4:e4b`; other Ollama models can be substituted by editing `MODEL_NAME` in `src/lx/ollama_client.py`)
- For clipboard support: a clipboard tool available to [`pyperclip`](https://pypi.org/project/pyperclip/): on Wayland, `wl-clipboard` (provides `wl-copy`); on X11, `xclip` or `xsel`

## Setup

```bash
git clone https://github.com/havl-code/lx.git
cd lx
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
ollama pull gemma4:e4b   # or your preferred model
```

## Usage

```bash
lx
```

You'll be prompted for a task in plain English. `lx` will show the generated command, an explanation, and a risk level, then ask if you'd like to copy the command to your clipboard. **It will never run the command for you.**

## Development

Install with dev dependencies (adds `pytest`):

```bash
pip install -e ".[dev]"
```

Run the test suite:

```bash
pytest
```

Tests cover JSON parsing/repair logic and CLI input validation, and run automatically on every push via GitHub Actions (see the badge above).

## Known limitations

- Small local models (4B to 8B class) don't always produce perfectly formed JSON. `lx` mitigates this with a repair step and retry logic, but it isn't foolproof: occasional failures are possible, especially with complex or unusual tasks.
- Risk classification is entirely the LLM's judgement based on prompt guidance. It's a helpful signal, not a guarantee. Always read the command and explanation yourself before running anything.
- `lx` is only available in terminals where its virtual environment is activated (standard for a project still in active development, not yet distributed as a system-wide tool).

## Roadmap

- [x] Package for proper installation (`pip install -e .`, `lx` as a console command)
- [x] Add automated tests for core logic
- [x] Add CI (GitHub Actions) to run tests on every push
- [x] Stream responses from Ollama instead of waiting for the full response
- [ ] Benchmark alternative models for speed/accuracy tradeoffs on CPU-only hardware
- [ ] Installable system-wide via `pipx`, without needing manual venv activation

## Licence

Released under the MIT Licence, see [LICENSE](LICENSE).
