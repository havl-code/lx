# Benchmarks

Informal benchmarking of locally available Ollama models against `lx`'s core task: turning a plain-English request into structured JSON (`command`, `explanation`, `risk`).

Run via `scripts/benchmark.py`, a standalone tool (not part of the installed `lx` package) that discovers your locally pulled models and times each one against a fixed set of five test tasks.

**Hardware:** Intel i7-1065G7 (4 cores / 8 threads), 16GB RAM, CPU-only inference (no dedicated GPU).

## Models tested

- `phi4-mini:3.8b`
- `llama3.2:3b`
- `gemma4:e4b` (the default model used by `lx`)

## Results

| Model | Avg time (s) | Fastest task | Slowest task | First-try JSON success |
|---|---|---|---|---|
| `phi4-mini:3.8b` | ~6.8 | 3.66s | 12.80s | 5/5 |
| `llama3.2:3b` | ~5.9 | 3.56s | 10.47s | 5/5 |
| `gemma4:e4b` | ~19.4 | 16.23s | 28.93s | 5/5 |

## Findings

**Speed:** the two smaller (~3-4B) models were consistently 2-4x faster than `gemma4:e4b` across every task, on CPU-only hardware, model size directly and substantially affects response latency, as expected.

**JSON reliability:** all three models produced valid, parseable JSON on the first attempt across all five tasks in this run. This is a single run, not a guarantee: earlier development testing showed `gemma4:e4b` occasionally failing to escape backslashes correctly inside JSON strings (see the JSON-repair logic in `parser.py`), a failure this specific run didn't happen to reproduce. JSON reliability appears to vary run-to-run, not purely by model.

**Command correctness (a more concerning finding):** even when JSON was valid, the *shell command itself* wasn't always correct or safe:
- `llama3.2:3b` produced a truncated, syntactically invalid command for the "delete old log files" task (`find /var/log -type f -mtime +30 -exec rm {} \`, missing the required `\;` or `+` terminator for `-exec`), while still labelling it "low risk". This is a real limitation worth taking seriously: valid JSON does not imply a valid or safe shell command.
- `phi4-mini:3.8b` occasionally wrapped its command in extraneous square brackets (`[find ... -delete]`), invalid as a literal shell command. This also surfaced a real bug in `lx` itself: square brackets in model output were being misinterpreted as Rich's own text-styling markup, silently corrupting the displayed command. Fixed by escaping model-generated text before rendering (see commit history).

## Takeaways

- Smaller models are meaningfully faster on CPU-only hardware, with no obvious JSON-reliability cost observed in this sample.
- Valid JSON structure does not guarantee a correct or runnable shell command; this reinforces why `lx` never auto-executes anything; a human reviewing the command before running it is a real safeguard, not a formality.
- Risk labels are a helpful signal from the model, not a verified guarantee, a "low risk" label was applied to a broken command in testing.

## Caveats

This is a small, informal benchmark (5 tasks, 3 models, single runs), not a rigorous statistical evaluation. Results may vary across hardware, Ollama versions, and model versions.