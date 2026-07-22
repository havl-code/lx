import sys
import time

sys.path.insert(0, "src")

import requests

from lx.ollama_client import list_available_models, get_structured_response, OllamaError
from lx.parser import ResponseParseError

TASKS = [
    "list all running processes",
    "show disk usage",
    "find every pdf larger than 50mb",
    "count the number of files in this folder",
    "delete all log files older than 30 days",
]

UNLOAD_PAUSE_SECONDS = 5


def unload_model(model: str) -> None:
    """Ask Ollama to unload a model from memory immediately."""
    try:
        requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": "", "keep_alive": 0},
            timeout=30,
        )
    except requests.exceptions.RequestException:
        pass  # best effort, don't crash the benchmark over a failed unload


def benchmark_model(model: str) -> list[dict]:
    """Run every task against one model, returning timing and outcome for each."""
    results = []
    for task in TASKS:
        start = time.perf_counter()
        try:
            result = get_structured_response(task, model)
            elapsed = time.perf_counter() - start
            results.append(
                {
                    "model": model,
                    "task": task,
                    "elapsed": elapsed,
                    "success": True,
                    "command": result["command"],
                    "risk": result["risk"],
                }
            )
        except (OllamaError, ResponseParseError) as exc:
            elapsed = time.perf_counter() - start
            results.append(
                {
                    "model": model,
                    "task": task,
                    "elapsed": elapsed,
                    "success": False,
                    "command": None,
                    "risk": None,
                    "error": str(exc),
                }
            )
    return results


def print_report(all_results: list[dict]) -> None:
    """Print a readable summary table of benchmark results."""
    print(f"\n{'Model':<20}{'Task':<45}{'Time (s)':<10}{'Result'}")
    print("-" * 95)
    for row in all_results:
        time_str = f"{row['elapsed']:.2f}"
        outcome = f"OK ({row['risk']})" if row["success"] else "FAILED"
        print(f"{row['model']:<20}{row['task']:<45}{time_str:<10}{outcome}")
        if row["success"]:
            print(f"    -> {row['command']}")
        else:
            print(f"    -> {row['error']}")


def main() -> None:
    models = list_available_models()
    print("Benchmarking against locally available models:")
    for name in models:
        print(f"  - {name}")
    print(
        "\nNOTE: models will be unloaded from memory between each one to avoid "
        "running multiple models simultaneously on limited RAM.\n"
    )

    all_results = []
    for i, model in enumerate(models):
        if i > 0:
            previous = models[i - 1]
            print(f"Unloading {previous} and pausing to let memory settle...")
            unload_model(previous)
            time.sleep(UNLOAD_PAUSE_SECONDS)

        print(f"\nRunning tasks against {model}...")
        all_results.extend(benchmark_model(model))

    # Unload the last model too, so nothing lingers in memory after the script ends
    unload_model(models[-1])

    print_report(all_results)


if __name__ == "__main__":
    main()