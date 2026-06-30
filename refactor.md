# 🔍 Code Review — ScuffedBot (AiAgent)

**First impression:** Solid foundation with a clean function-calling architecture. The main issues are dead code, hardcoded configuration, inconsistent error handling, and ad-hoc test scripts that should be proper test suites.

---

## `main.py`

- **L28-31**: 🟡 risk: Commented-out blocks (ChatInputApp import, one_shot check). Dead code confuses readers. Remove commented blocks.
- **L37**: 🔵 nit: Variable `input` shadows built-in `input()`. Rename to `prompt` or `user_input`.
- **L52**: 🔵 nit: Magic number `range(20)`. Extract to a module-level constant `MAX_LOOP_ITERATIONS = 20`.
- **L54**: 🔵 nit: Redundant type annotation `resp: Response | None` on reassignment. Already typed at L35. Drop the annotation.
- **L65-72**: 🔵 nit: `if len(function_calls) > 0:` / `elif len(function_calls) == 0:`. Use `if function_calls:` then `else:`. The `elif` is logically an `else`.
- **L74**: 🟡 risk: `for/else` on line 74 fires when max iterations hit (loop exhausted without break). The message says "Error: max iterations reached" but printed via `console.print` while everything else uses `Panel`. Also the `else:` clause is easily mistaken for the inner `if/elif/else`. Extract iteration limit logic into a clearer pattern: add a `break` with a flag when max reached.
- **L108**: 🔵 nit: `if len(function_result_outputs) > 0:`. Use `if function_result_outputs:`.
- **L115**: 🔵 nit: `if function_calls and len(function_calls) > 0:`. The `len()` check is redundant after truthy check. Use `if function_calls:`.

---

## `response.py`

- **L23**: 🟡 risk: Model hardcoded to `"inception/mercury-2:nitro"`. Should be configurable via env var (`MODEL_NAME`) or a config module, not baked into source.
- **L13-15**: 🔵 nit: `if api_key is None:` check. `load_dotenv()` may fail silently. Use `os.getenv("OPENROUTER_API_KEY") or raise RuntimeError(...)` in one expression.
- **L29-30**: ❓ q: `if not resp:` guard — will `responses.create()` ever return None vs raising? If the SDK raises on failure, this is dead code.

---

## `custom_args.py`

- **L8**: 🔵 nit: Parser description `"Basic call, response chatbot"` is inaccurate for an AI agent with function calling. Update to `"AI coding agent with file operations and function calling"`.
- **L11**: 🟡 risk: `--one-shot` help says "Single response mode, no history" but the flag handling is completely commented out in `main.py`. Either un-dead-code the feature or remove the flag and its help.
- **L22**: 🔵 nit: `console.print(args.__dict__)` — prefer `vars(args)` over accessing `__dict__` directly.

---

## `input.py` (TUI)

- **L62**: 🔵 nit: `self.history: ResponseInputParam = []` — fine for initialization but `ResponseInputParam` is a complex union type. Consider a comment noting the expected shape.
- **L70-87**: 🟡 risk: No API timeout handling. If `get_response()` hangs, the TUI is frozen with LoadingIndicator visible forever. Add `asyncio.wait_for(resp, timeout=30)` or pass a timeout downstream.
- **L81**: 🔵 nit: Uses `resp.output_text` — this is the aggregated text from the Response. Works but should verify the Response actually has text (not just tool calls) before displaying.

---

## `call_function.py`

- **L40-41**: 🔵 nit: Uses bare `print()` instead of `console.print()` from rich. Inconsistent with the rest of the codebase which uses rich console for all output.
- **L52**: 🟡 risk: Hardcoded `"./calculator"` as working_directory. This means ALL function calls operate within a fixed subdirectory. Should be configurable via env var or CLI arg (e.g., `--workdir`).
- **L53**: 🟡 risk: `function_args["working_directory"] = "./calculator"` silently overrides any value the caller or AI might provide. The parameter becomes a lie. Either remove it from the function signature and inject it, or make it actually configurable.
- **L37-38**: 🔵 nit: `json.JSONDecodeError` caught silently — malformed args become `{}` with no warning. Log a debug message when this happens.

---

## `functions/get_file_content.py`

- **L28**: 🔵 nit: `f.read(1)` to detect truncation works but is fragile (read position shifts). Prefer `os.path.getsize(target_file) > MAX_CHARS` before reading.
- **L34-37**: 🟡 risk: Only catches `PermissionError` and `FileNotFoundError`. Missing `IOError`, `OSError`, `UnicodeDecodeError` for binary files. Add a broad `Exception` catch or specific `OSError`.

---

## `functions/get_files_info.py`

- **L6**: 🔵 nit: Missing type annotations for `working_directory` and `directory` parameters. Annotate as `def get_files_info(working_directory: str, directory: str = ".")` to match the other function files.
- **L23-24**: 🟡 risk: `os.path.exists()` check placed AFTER `os.path.isdir()` check. If path doesn't exist, `os.path.isdir()` returns False, so `NotADirectoryError` fires before `FileNotFoundError`. The `FileNotFoundError` is dead code. Fix order: `exists()` → `isdir()` → listdir.

---

## `functions/run_python_file.py`

- **L32**: 🔴 bug: `subprocess.run(..., timeout=30)` raises `subprocess.TimeoutExpired` which is not caught. Any process running >30s crashes the agent. Add a `except subprocess.TimeoutExpired` handler.
- **L33-39**: 🔵 nit: String concatenation for output building. Use an f-string or `io.StringIO` for readability.
- **L42-47**: 🟡 risk: Missing `subprocess.TimeoutExpired` and `OSError` catches. Add them.

---

## `functions/write_file.py`

- **L11-13**: 🟡 risk: Only validates that the _parent directory_ of the target is within the working dir. The target file itself isn't validated. If parent_dir is inside but file_path uses `../` within the parent, it could escape. Add validation on the full resolved `target_file` too.
- **L24**: 🔵 nit: `os.makedirs(parent_dir, exist_ok=True)` creates dirs silently. Consider a verbose log when new directories are created.

---

## Test Files (all 4)

- **`test_*.py` all files**: 🔴 bug: These are ad-hoc print scripts, not proper unit tests. They use no test framework (`unittest`, `pytest`). Run manually — they never fail CI because there's no CI. Convert to `pytest` with `assert` statements and register in `pyproject.toml`.
- **`test_get_file_content.py:L10`**: 🔴 bug: Calls `get_file_content("calculator", "lorem.txt")` — but `call_function.py` hardcodes `working_directory="./calculator"`. When called via the agent, the effective path is `./calculator/calculator/lorem.txt`, which doesn't exist. The test doesn't match runtime behavior.
- **`test_write_file.py:L5-6`**: 🔴 bug: Tests write to actual fixture files (`calculator/lorem.txt`, `calculator/pkg/morelorem.txt`), mutating test data. Use `tempfile.TemporaryDirectory` instead.
- **`test_get_file_content.py:L10`**: 🟡 risk: `test_cases` includes `("calculator", "/bin/cat")` for path traversal testing — good, but `("calculator", "main.py")` vs `("calculator", "pkg/calculator.py")` — the second test's description says `pkg/calculator.py` but the result is never verified. Add `assert` statements.
- **`test_run_python_file.py:L8`**: 🟡 risk: Tests `("../main.py")` path traversal but never asserts the result. Add assertions.

---

## `calculator/pkg/calculator.py`

- **L18**: 🔵 nit: `evaluate()` returns `None` (empty expression) or `float`. Inconsistent return type. Either raise `ValueError` for empty input to match the other error paths, or annotate as `-> float | None`.
- **L46-48**: 🔵 nit: Generic `"invalid expression"` error. Include what was in `values` or tokens for debugging.

---

## `calculator/pkg/render.py`

- **L7**: ❓ q: `isinstance(result, float) and result.is_integer()` — converts int-like floats to int. If the result is a true int (e.g., from future changes), the `isinstance` check fails and it stays as int. Works currently, but fragile. Consider `isinstance(result, (int, float))`.

---

## Configuration & Project Structure

- **`config.py`**: 🔵 nit: Only has `MAX_CHARS = 10000`. Underutilized config module. Move all magic numbers and hardcoded strings here: model name, max iterations, working directory, API base URL.
- **`pyproject.toml`**: 🟡 risk: No `[tool.pytest.ini_options]` section, no test runner configured. Add pytest config and a `[project.scripts]` entry for `uv run main.py`.
- **`calculator/pkg/morelorem.txt`**: 🔵 nit: This is a leftover from the write test. Tracked in git? If not, add to `.gitignore`. If yes, remove from repo.
- **`functions/` and `calculator/pkg/`**: 🔵 nit: Missing `__init__.py` files. Python 3.3+ supports namespace packages, but adding explicit `__init__.py` prevents subtle import issues and documents the package structure.

---

## Top 3 Most Important Changes

1. **🔴 Bug (test/behavior mismatch):** `test_get_file_content.py:L10` tests with `working_directory="calculator"` but `call_function.py:L52` hardcodes `"./calculator"`, creating a doubled path when the agent actually runs. Fix the hardcoded workdir or fix the tests.
2. **🔴 Bug (unhandled exception):** `run_python_file.py:L32` — `subprocess.run(timeout=30)` can raise `TimeoutExpired`, crashing the agent. Add a handler.
3. **🟡 Risk (hardcoded config):** Model name (`response.py:L23`), working directory (`call_function.py:L52`), and max iterations (`main.py:L52`) are all hardcoded. Move to `config.py` or env vars for configurability.
