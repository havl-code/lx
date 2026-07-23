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

## Follow-up finding: nested quoting and JSON reliability

A later real-world test task, "change all file extensions in a folder from .png to .jpg", surfaced a deeper reliability issue than the earlier backslash-escaping bug.

This task naturally requires a shell command with **nested quoting**: a pattern like `bash -c 'mv "$file" "${file%.png}.jpg"'` needs both single quotes (for the outer `-c` argument) and double quotes (for variable expansion inside it). Representing that correctly as a JSON string value requires escaping the inner double quotes (`\"`), something `phi4-mini:3.8b` failed to do consistently, across multiple attempts, multiple retries, and even after:

- Prompt engineering specifically warning about quote escaping
- Enabling Ollama's `"format": "json"` constrained-decoding option, which forces syntactically valid JSON at the token level

With `format: json` enabled, `phi4-mini` did produce syntactically valid JSON, but at the cost of dropping the `explanation` and `risk` fields entirely on this particular task, suggesting the model was already at its structural limit for the combined demands of this task (correct nested quoting *and* the full three-field schema).

`gemma4:e4b` (the larger model) succeeded on the same task, first attempt, no retries needed, producing a simpler `for` loop instead of a nested `bash -c` pattern, both correctly escaped in JSON *and* structurally simpler to begin with.

**Takeaway:** for tasks requiring nested shell quoting, smaller local models (here, ~3.8B) may be unable to reliably produce valid structured output, even with strong prompt engineering and format constraints. Larger models may succeed both by escaping correctly and by naturally choosing simpler, less quote-heavy command structures. This is a genuine capability ceiling, not something `lx`'s repair/retry logic can fully paper over, and is now documented as a known limitation.

## Takeaways

- Smaller models are meaningfully faster on CPU-only hardware, with no obvious JSON-reliability cost observed in this sample.
- Valid JSON structure does not guarantee a correct or runnable shell command; this reinforces why `lx` never auto-executes anything; a human reviewing the command before running it is a real safeguard, not a formality.
- Risk labels are a helpful signal from the model, not a verified guarantee, a "low risk" label was applied to a broken command in testing.

## Caveats

This is a small, informal benchmark (5 tasks, 3 models, single runs), not a rigorous statistical evaluation. Results may vary across hardware, Ollama versions, and model versions.