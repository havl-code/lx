**lx** turns plain-English task descriptions into ready-to-use Linux commands — powered entirely by a local LLM (via [Ollama](https://ollama.com)), so it's private, free, and works offline. It **never runs anything automatically** — you always stay in control.

## Why

I don't want to memorize every Linux command flag, and I don't want an AI agent auto-executing commands on my machine without me reviewing them first. `lx` is a small, focused tool built around one idea: **an LLM is great at generating a command from a description, but a human should always be the one who decides whether to run it.**

## Design decisions

- **100% local, no cloud APIs.** Everything runs through Ollama on your own machine — nothing is sent anywhere, and there's no API cost.
- **Never auto-executes.** `lx` only displays a command, an explanation, and a risk level. Copying it to your clipboard is the only optional action it takes, and only with explicit confirmation.
- **Structured, reliable output.** The LLM is prompted to return strict JSON (`command`, `explanation`, `risk`). Since small local models don't always follow formatting instructions perfectly, `lx` includes a JSON-repair step (for common escaping mistakes) and automatic retry logic if parsing still fails.
- **Risk labeling.** Every generated command is labeled `low`, `medium`, or `high` risk, and color-coded in the terminal (green/yellow/red), so dangerous commands are visually distinct before you ever consider running them.

## Requirements

- Linux (developed and tested on CachyOS/Arch)
- Python 3.11+
- [Ollama](https://ollama.com) installed and running
- A pulled model (developed against `gemma4:e4b`; other Ollama models can be substituted by editing `MODEL_NAME` in `src/lx/ollama_client.py`)
- For clipboard support: a clipboard tool available to [`pyperclip`](https://pypi.org/project/pyperclip/) — on Wayland, `wl-clipboard` (provides `wl-copy`); on X11, `xclip` or `xsel`

## Setup

```bash
git clone <your-repo-url>
cd lx
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ollama pull gemma4:e4b   # or your preferred model
```

## Usage

```bash
PYTHONPATH=src python src/lx/main.py
```

> **Note:** the `PYTHONPATH=src` prefix is a known rough edge — this project isn't packaged for installation yet (planned; see Roadmap below). Once packaged, this will simplify to a plain `lx` command.

You'll be prompted for a task in plain English. `lx` will show the generated command, an explanation, and a risk level, then ask if you'd like to copy the command to your clipboard. **It will never run the command for you.**

## Known limitations

- Small local models (4B–8B class) don't always produce perfectly formed JSON. `lx` mitigates this with a repair step and retry logic, but it isn't foolproof — occasional failures are possible, especially with complex or unusual tasks.
- Risk classification is entirely the LLM's judgment based on prompt guidance — it's a helpful signal, not a guarantee. Always read the command and explanation yourself before running anything.
- Currently requires manual `PYTHONPATH` configuration to run (see Setup/Usage above).

## Roadmap

- [ ] Package for proper installation (`pip install -e .`, `lx` as a console command)
- [ ] Benchmark alternative models for speed/accuracy tradeoffs on CPU-only hardware

## License

MIT
