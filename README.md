# lx

[![Tests](https://github.com/havl-code/lx/actions/workflows/tests.yml/badge.svg)](https://github.com/havl-code/lx/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

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
- **Structured, reliable output.** The LLM is prompted to return strict JSON (`command`, `explanation`, `risk`), with a worked example included in the prompt (few-shot prompting) to improve reliability on trickier tasks. Since small local models don't always follow formatting instructions perfectly, `lx` also includes a JSON-repair step (for common escaping mistakes), Ollama's `format: json` constrained decoding, and automatic retry logic if parsing still fails.
- **A syntax-check safety net.** Before displaying a generated command, `lx` runs a dry-run bash parse (`bash -n`, nothing is executed) and shows a warning if the command fails basic syntax validation.
- **Risk labelling.** Every generated command is labelled `low`, `medium`, or `high` risk, and colour-coded in the terminal (green/yellow/red), so dangerous commands are visually distinct before you ever consider running them.
- **Streamed under the hood.** Responses are read from Ollama as a stream of chunks rather than one blocking call, with a live animated status indicator while the model works. The final result is still shown all at once (not word-by-word), since a partially-generated command or JSON fragment isn't meaningful or safe to display mid-stream.
- **Model choice, your call.** On startup, `lx` lists every model you've pulled locally via Ollama and lets you pick one interactively. Set the `LX_MODEL` environment variable to skip the picker and always use a specific model.
- **Tested and CI-checked.** Core logic (JSON parsing/repair, input validation, display rendering, clipboard behaviour) has unit tests, run automatically via GitHub Actions on every push.

## Requirements

- Linux (developed and tested on CachyOS/Arch)
- Python 3.11+
- [Ollama](https://ollama.com) installed and running, with at least one model pulled (e.g. `ollama pull gemma4:e4b`)
- For clipboard support: a clipboard tool available to [`pyperclip`](https://pypi.org/project/pyperclip/): on Wayland, `wl-clipboard` (provides `wl-copy`); on X11, `xclip` or `xsel`

## Setup

Recommended, install as a standalone command available in any terminal:

```bash
git clone https://github.com/havl-code/lx.git
cd lx
pipx install --editable .
ollama pull gemma4:e4b   # or any model you prefer
```

Alternatively, for development (running tests, editing dependencies), use a virtual environment instead:

```bash
git clone https://github.com/havl-code/lx.git
cd lx
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
ollama pull gemma4:e4b
```

## Usage

```bash
lx
```

You'll be shown a list of your locally available Ollama models to choose from, then prompted for a task in plain English. `lx` will show the generated command, an explanation, and a risk level, then ask if you'd like to copy the command to your clipboard. **It will never run the command for you.**

To skip the model picker and always use a specific model:

```bash
LX_MODEL=gemma4:e4b lx
```

## Development

Install with dev dependencies (adds `pytest` and `matplotlib`):

```bash
pip install -e ".[dev]"
```

Run the test suite:

```bash
pytest
```

Tests cover JSON parsing/repair logic, CLI input validation, display rendering (including a regression test for a real markup-escaping bug), and clipboard behaviour, and run automatically on every push via GitHub Actions (see the badge above).

### Benchmarking models

`scripts/benchmark.py` times a fixed set of tasks against every locally pulled Ollama model, checks JSON-parsing reliability and basic command syntax validity, and generates a comparison chart. See [BENCHMARKS.md](BENCHMARKS.md) for results and findings from testing on this project's development hardware, including a follow-up investigation into few-shot prompting and syntax checking as reliability improvements.

```bash
python scripts/benchmark.py
```

## Known limitations

- Small local models (3B to 8B class) don't always produce perfectly formed JSON. `lx` mitigates this with a repair step, retry logic, few-shot prompting, and Ollama's `format: json` constraint, but it isn't foolproof: occasional failures are still possible, especially for tasks requiring nested shell quoting (e.g. a command that itself needs both single and double quotes). See [BENCHMARKS.md](BENCHMARKS.md) for documented examples.
- Valid JSON doesn't guarantee a correct or safe shell command; benchmarking surfaced real cases of syntactically broken or semantically incorrect commands, in some cases labelled "low risk". Always read the command and explanation yourself before running anything.
- Risk classification is entirely the LLM's judgement based on prompt guidance, and can vary between runs for similar commands. It's a helpful signal, not a guarantee.
- `lx` is only available in terminals where it's been installed (via `pipx` or an activated venv), see Setup above.
- Generated commands are checked for basic bash syntax validity (via `bash -n`) before being shown, and a warning is displayed if a command fails this check. This catches bash grammar errors (e.g. unbalanced quotes) but not command-specific argument errors (e.g. a missing required argument to `find -exec`), see [BENCHMARKS.md](BENCHMARKS.md) for a real example of each.

## Roadmap

- [x] Package for proper installation (`pip install -e .`, `lx` as a console command)
- [x] Add automated tests for core logic
- [x] Add CI (GitHub Actions) to run tests on every push
- [x] Stream responses from Ollama instead of waiting for the full response
- [x] Interactive model selection, with an `LX_MODEL` override
- [x] Benchmark alternative models for speed/accuracy tradeoffs on CPU-only hardware
- [x] Installable system-wide via `pipx`, without needing manual venv activation
- [x] Investigate whether smaller models can be made more reliable for nested-quoting tasks (few-shot prompting, plus a bash syntax-check safety net)

## Acknowledgments

Built with guidance from Claude (Anthropic), used as a mentor throughout development: explaining concepts, reviewing code, and helping diagnose real bugs along the way.

## Licence

Released under the MIT Licence, see [LICENSE](LICENSE).