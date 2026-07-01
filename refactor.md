# 🔍 Code Review — ScuffedBot (AiAgent)

**Last reviewed:** 2026-07-01 (post-refactor)

**Status:** Core issues addressed. Remaining items are test infrastructure, calculator nits, and project structure.

---

## ✅ Fixed Issues

### Critical Bugs (all resolved)
- **`run_python_file.py`** — `subprocess.TimeoutExpired` now caught; `OSError` handler added; uses `sys.executable` instead of bare `"python"` (venv-safe).
- **`input.py`** — TUI now processes function calls (tool-call loop matching `main.py`); history corruption on error fixed (pops user message on failure).
- **`call_function.py`** — Working directory override fixed (`"."` instead of `"./calculator"`); function dispatch wrapped in try/except; bare `print()` replaced with `rich` console; JSON decode errors now logged.

### Risks (resolved)
- **`main.py`** — Dead code removed (8 commented-out lines); `input` variable renamed to `user_prompt`; magic number `20` replaced with `MAX_ITERATIONS` from config; unreachable `else` replaced with proper `for/else` exhaustion pattern; redundant `len() > 0` checks simplified.
- **`response.py`** — Model name and base URL centralized in `config.py`; `load_dotenv()` moved into function body (no more import-time side effects); dead `if not resp` guard removed; param renamed to `input_messages` (no longer shadows builtin).
- **`custom_args.py`** — Parser description updated; `--one-shot` help text corrected; `vars(args)` used instead of `args.__dict__`.
- **`input.py`** — API timeout added (`asyncio.wait_for`); `/clear` command added; welcome message on mount; double-submit fix (removed `BINDINGS`); `auto_scroll=True` on RichLog.
- **`get_files_info.py`** — Error check order fixed (`exists()` before `isdir()`); type annotations added; tool description corrected ("directory to list"); `OSError` guard added in loop.
- **`get_file_content.py`** — `encoding="utf-8"` added; `OSError` and `UnicodeDecodeError` handlers added.
- **`write_file.py`** — Full path validation (not just parent dir); symlink escape fixed via `os.path.realpath()`; `encoding="utf-8"` added; `OSError` handler added.

### Config Centralization
All hardcoded values moved to `config.py`:
- `MODEL_NAME` (env-overridable via `MODEL_NAME` env var)
- `MAX_ITERATIONS`, `WORKING_DIRECTORY`, `API_BASE_URL`
- `SUBPROCESS_TIMEOUT`, `TUI_TIMEOUT`, `MAX_CHARS`

---

## 🔴 Remaining Critical Issues

### Test Files (all 4 `test_*.py`)
- **Ad-hoc print scripts**, not proper unit tests. No test framework (`pytest`/`unittest`), no assertions. Run manually — never fail CI because there is no CI.
- **`test_write_file.py`** — Mutates actual fixture files (`calculator/lorem.txt`, `calculator/pkg/morelorem.txt`). Should use `tempfile.TemporaryDirectory`.
- **`test_run_python_file.py`** / **`test_get_file_content.py`** — Traversal cases print results but never assert.
- **Fix:** Convert all 4 to `pytest` with `assert` statements. Add `pytest` to dev dependencies. Add `[tool.pytest.ini_options]` to `pyproject.toml`.

---

## 🟡 Remaining Risks

### `response.py`
- **Client re-instantiated per call** — `AsyncOpenAI` is created inside `get_response()` on every invocation. No connection pooling/reuse. Low priority (OpenRouter handles this server-side) but could hoist to module scope if performance matters.

### `call_function.py`
- **Inconsistent output shape** — Unknown function returns `{"error": ...}`; success returns `{"result": ...}`. The model sees two different schemas. Consider unifying.
- **Silent working_directory override** — `function_args["working_directory"] = WORKING_DIRECTORY` silently overrides any value the model supplies. Acceptable since `prompts.py` tells the model not to send it, but if it does, it's silently discarded.

### `main.py`
- **`json.loads(call.arguments)`** (line ~110) in the verbose-display path has no guard. `call.arguments` can be `None` or malformed JSON → uncaught `TypeError`/`JSONDecodeError`. `call_function.py` defends against this, but `main.py`'s display path does not.

### `custom_args.py`
- **Import-time `parse_args()`** — `args = parser.parse_args()` runs at import time, consuming `sys.argv`. Makes `custom_args` un-importable from tests without argv manipulation. Defer parsing to a function.

---

## 🔵 Remaining Nits

### Project Structure
- **Missing `__init__.py`** — `functions/` and `calculator/pkg/` lack `__init__.py` files. Namespace packages work in Python 3.3+ but explicit packages prevent subtle import issues.
- **`calculator/pkg/morelorem.txt`** — Leftover from write test, tracked in git. Remove from repo or add to `.gitignore`.
- **`pyproject.toml`** — No `[tool.pytest.ini_options]` section; no `[project.scripts]` entry.

### `calculator/pkg/calculator.py`
- **`evaluate()`** returns `None` (empty input) or `float`. Inconsistent return type — annotate as `-> float | None`.
- **Generic error message** — "invalid expression" doesn't include the problematic tokens for debugging.

### `calculator/pkg/render.py`
- **`isinstance(result, float)`** — Fragile if result is ever a true `int`. Consider `isinstance(result, (int, float))`.

### `prompts.py`
- **Leading `\n`** in triple-quoted string — cosmetic only.

### `response.py`
- **`# type: ignore[arg-type]`** — Papers over a real type mismatch: signature is `Sequence[ResponseInputItem]` (pydantic models) but SDK wants `ResponseInputParam` (dicts). Works at runtime via SDK serialization; type-system lie.

### Doc Mismatch
- **`AGENTS.md`** claims "Defaults to `openrouter/free` in `response.py`"; actual model is `inception/mercury-2:nitro` (now configurable via `MODEL_NAME` env var). Update AGENTS.md.

---

## Top 3 Remaining Priorities

1. **🔴 Test infrastructure** — Convert 4 ad-hoc test scripts to proper `pytest` tests with assertions and `tempfile` usage. Add pytest to dev dependencies.
2. **🟡 `main.py` verbose path** — Add try/except around `json.loads(call.arguments)` in the display path.
3. **🟡 `custom_args.py`** — Defer `parse_args()` to a function to make the module importable from tests.
