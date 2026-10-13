# Python `os` and `sys`: what they are, why they matter, what to master

Part 4 of the API connection study series · 13 October 2026 · Python 3.10+ (examples run on Python 3.14, Windows)

Related: [Part 1 — API authentication concepts](API_AUTHENTICATION_STUDY_GUIDE.md) (section 11 is the short version of this guide) · [Part 2 — Azure/GCP identity setup](AZURE_GCP_IDENTITY_SETUP_GUIDE.md) · [Part 3 — Personal Access Tokens](PERSONAL_ACCESS_TOKENS_GUIDE.md)

**In one sentence:** `os` is how your Python code talks to the **operating system** (environment variables, files, folders, processes), and `sys` is how it talks to **the Python interpreter that is running it** (arguments, exit codes, import paths, version, standard streams). Almost every real script — API clients, data pipelines, notebooks, CLIs — needs both, because configuration and secrets arrive through the environment and problems are diagnosed through the interpreter.

All examples use placeholder variable names. No real keys or passwords appear, and none should ever be printed.

## Contents

1. [What they are](#1-what-they-are)
2. [Why they are so important](#2-why-they-are-so-important)
3. [`os`: the functions to master](#3-os-the-functions-to-master)
4. [`os.path`: working with file paths](#4-ospath-working-with-file-paths)
5. [`sys`: the attributes and functions to master](#5-sys-the-attributes-and-functions-to-master)
6. [Modern companions: pathlib, shutil, subprocess, argparse, secrets](#6-modern-companions-pathlib-shutil-subprocess-argparse-secrets)
7. [Seven worked examples](#7-seven-worked-examples)
8. [Pitfalls and how to avoid them](#8-pitfalls-and-how-to-avoid-them)
9. [Must-master cheat sheet](#9-must-master-cheat-sheet)
10. [Practice questions and answers](#10-practice-questions-and-answers)

---

## 1. What they are

Both are **standard-library modules**: they ship with every Python installation. `import os` and `import sys` load them; there is nothing to `pip install`.

| | `os` | `sys` |
|---|---|---|
| Talks to | The **operating system** (Windows, Linux, macOS) | The **Python interpreter** itself |
| Typical questions it answers | "What is the value of `API_KEY` in my environment?" "Does this folder exist?" "List the CSV files here." | "Which Python is running?" "What arguments was my script given?" "Where does Python look for modules?" "Exit with an error code." |
| Key pieces | `os.environ`, `os.getenv`, `os.getcwd`, `os.listdir`, `os.walk`, `os.makedirs`, `os.remove`, `os.replace`, `os.path.*` | `sys.argv`, `sys.exit`, `sys.path`, `sys.executable`, `sys.version_info`, `sys.platform`, `sys.stdout`, `sys.stderr`, `sys.modules` |
| Cross-platform? | Yes — it hides OS differences (path separators, environment APIs) | Yes |

A useful picture:

```
 Your script
    │
    ├── sys ──► the Python interpreter  (version, argv, import path, stdout/stderr, exit code)
    │
    └── os ───► the operating system     (environment variables, files, folders, process info)
                    │
                    └── os.path ─► string-based file path helpers
```

---

## 2. Why they are so important

1. **Configuration and secrets arrive through the environment.** Twelve-factor apps, Docker, Kubernetes, GitHub Actions, Azure App Service, Cloud Run, Databricks jobs and Fabric all inject settings as **environment variables**. `os.environ` / `os.getenv` is how your code reads them — and therefore how you keep keys **out of source code** (Part 1, sections 3–8).
2. **Code must run on more than one machine.** `os.path.join`, `os.sep` and `os.makedirs(..., exist_ok=True)` make the same script work on your Windows laptop and a Linux container.
3. **"It works on my machine" is almost always an interpreter problem.** `sys.executable`, `sys.version_info` and `sys.path` tell you *which* Python and *which* packages are actually in use — the first thing to check when `ModuleNotFoundError` appears.
4. **Scripts need to behave like proper command-line tools.** `sys.argv` receives arguments, `sys.exit(code)` tells schedulers and CI whether the run succeeded, `sys.stderr` separates errors from data output.
5. **Data pipelines are file-heavy.** Listing landing folders, creating output directories, atomically replacing files and checking sizes and timestamps are all `os` / `os.path` (or `pathlib`) work.
6. **Diagnostics and security reviews.** Knowing what the process can see (environment, working directory, platform) is how you debug and how you avoid leaking secrets (never print `os.environ`).

---

## 3. `os`: the functions to master

### 3.1 Environment variables — the most important part

| Call | What it does | When value missing |
|---|---|---|
| `os.environ["NAME"]` | Read a **required** variable | Raises `KeyError` — good: fail fast |
| `os.getenv("NAME")` | Read an **optional** variable | Returns `None` |
| `os.getenv("NAME", "default")` | Optional with default | Returns `"default"` (but **not** if the variable exists and is empty `""`) |
| `os.environ.get("NAME", "default")` | Same as `getenv` | Same |
| `"NAME" in os.environ` | Test presence | `False` |
| `os.environ["NAME"] = "value"` | Set for **this process and its children** | — |
| `os.environ.setdefault("NAME", "v")` | Set only if not already set | — |
| `os.environ.pop("NAME", None)` / `del os.environ["NAME"]` | Remove | — |
| `os.environ.copy()` | Snapshot dict — e.g. to build a child process environment | — |

```python
import os

API_BASE = os.environ["API_BASE"].rstrip("/")            # required
TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))            # optional number: convert explicitly
DEBUG = os.getenv("DEBUG", "false").strip().lower() in {"1", "true", "yes", "on"}  # parse booleans explicitly
API_KEY = os.getenv("API_KEY")
if not API_KEY:                                          # catches missing AND empty
    raise RuntimeError("API_KEY is missing or empty")
```

Rules:

- **Every value is a string.** Convert with `int()`, `float()`, explicit boolean parsing. `bool("false")` is `True`.
- Setting `os.environ[...]` affects **only the current Python process and processes it starts** — never the terminal that launched it, never other notebooks or sessions.
- Environment variables are a **delivery mechanism, not a vault**. Load them from a vault (Key Vault, Secret Manager, GitHub secrets) or a local `.env` file that is git-ignored.
- **Never** `print(os.environ)` or log it — it usually contains tokens.

How to set variables before launching Python:

```powershell
# PowerShell (current window only)
$env:API_BASE = "https://api.example.com"
python app.py
```

```bash
# bash / zsh
export API_BASE="https://api.example.com"
python app.py
# or for a single command:
API_BASE="https://api.example.com" python app.py
```

### 3.2 Working directory

| Call | Use |
|---|---|
| `os.getcwd()` | Current working directory — where **relative** paths are resolved |
| `os.chdir(path)` | Change it (avoid in libraries and notebooks: it changes global state for everything else) |

The working directory is **where Python was started from**, not where your script lives. To find files next to your script, use `os.path.dirname(os.path.abspath(__file__))` or `Path(__file__).resolve().parent` (notebooks usually have no `__file__`).

### 3.3 Files and directories

| Call | Use | Notes |
|---|---|---|
| `os.listdir(path)` | Names in a folder | Names only, unsorted |
| `os.scandir(path)` | Iterator of entries with `.name`, `.path`, `.is_file()`, `.stat()` | Faster than `listdir` + `stat`; use as context manager |
| `os.walk(top)` | Recursively yields `(dirpath, dirnames, filenames)` | The classic "find every file under a folder" |
| `os.makedirs(path, exist_ok=True)` | Create a folder and all parents | `exist_ok=True` avoids an error if it already exists |
| `os.mkdir(path)` | Create one folder | Parent must exist |
| `os.remove(path)` / `os.unlink(path)` | Delete a file | Irreversible — no recycle bin |
| `os.rmdir(path)` | Delete an **empty** folder | Use `shutil.rmtree` for non-empty (carefully) |
| `os.rename(src, dst)` | Rename / move | Fails on Windows if `dst` exists |
| `os.replace(src, dst)` | Rename, **overwriting** `dst` atomically | Use for safe "write temp file then swap" |
| `os.stat(path)` | Size (`st_size`), modified time (`st_mtime`), mode… | |
| `os.chmod(path, mode)` | Permissions (POSIX meaning; limited on Windows) | e.g. `0o600` for a private key file on Linux |

### 3.4 Process and platform information

| Call | Returns | Typical use |
|---|---|---|
| `os.name` | `"nt"` (Windows) or `"posix"` | Branch on platform (prefer `sys.platform` for detail) |
| `os.sep`, `os.pathsep`, `os.linesep` | `\` or `/`; `;` or `:`; `\r\n` or `\n` | Rarely needed directly if you use `os.path.join` / `pathlib` |
| `os.getpid()` | Current process ID | Logging, lock files |
| `os.cpu_count()` | Number of CPUs | Size thread / process pools |
| `os.devnull` | `"nul"` / `"/dev/null"` | Discard output |
| `os.urandom(n)` | `n` cryptographically secure random bytes | Prefer the `secrets` module for tokens (section 6) |
| `os.system(cmd)` | Runs a shell command | **Avoid** — use `subprocess.run([...])` (no shell injection, captures output) |

---

## 4. `os.path`: working with file paths

`os.path` works on **strings**. (`pathlib`, section 6, is the modern object-based alternative; both are fine — be consistent.)

| Call | Example | Result |
|---|---|---|
| `os.path.join(a, b, …)` | `os.path.join("data", "raw", "sales.csv")` | `data\raw\sales.csv` on Windows, `data/raw/sales.csv` on Linux |
| `os.path.exists(p)` | | `True` for file or folder |
| `os.path.isfile(p)` / `os.path.isdir(p)` | | Type-specific checks |
| `os.path.abspath(p)` | `os.path.abspath("data")` | Full path from the working directory |
| `os.path.realpath(p)` | | Absolute path with symlinks resolved |
| `os.path.basename(p)` | `".../raw/sales.csv"` | `sales.csv` |
| `os.path.dirname(p)` | `".../raw/sales.csv"` | `.../raw` |
| `os.path.split(p)` | | `(dirname, basename)` |
| `os.path.splitext(p)` | `"sales.2026.csv"` | `("sales.2026", ".csv")` |
| `os.path.getsize(p)` | | Bytes |
| `os.path.getmtime(p)` | | Last-modified time (epoch seconds) |
| `os.path.expanduser("~/x")` | | `C:\Users\you\x` or `/home/you/x` |
| `os.path.expandvars("$HOME/x")` | | Substitutes environment variables in a string |
| `os.path.normpath(p)` | `"a/./b/../c"` | `a\c` / `a/c` |
| `os.path.relpath(p, start)` | | Path relative to `start` |

**Do not** use `os.path.join` to build URLs: on Windows it inserts backslashes. Use string formatting or `urllib.parse.urljoin` for URLs.

---

## 5. `sys`: the attributes and functions to master

### 5.1 Interpreter identity — "which Python is this?"

| Attribute | Example value | Why you need it |
|---|---|---|
| `sys.executable` | `C:\Users\you\proj\.venv\Scripts\python.exe` | Proves which interpreter (and therefore which installed packages) is running |
| `sys.version` / `sys.version_info` | `3.12.4 (...)` / `(3, 12, 4, 'final', 0)` | Version checks: `if sys.version_info < (3, 10): sys.exit("Python 3.10+ required")` |
| `sys.platform` | `win32`, `linux`, `darwin` | OS-specific behaviour |
| `sys.prefix` vs `sys.base_prefix` | different inside a venv | `sys.prefix != sys.base_prefix` → you're inside a virtual environment |
| `sys.modules` | dict of loaded modules | Check whether something was already imported; debugging import side effects |

The classic fix for "I installed it but Python can't find it": install with the **same** interpreter that runs your code:

```powershell
python -c "import sys; print(sys.executable)"
python -m pip install requests        # 'python -m pip' guarantees the same interpreter
```

In Jupyter/Fabric/Databricks notebooks use `%pip install package` for the same reason.

### 5.2 `sys.path` — where imports are searched

- A list of folders Python searches for `import x`, in order: the script's folder (or `""` for the working directory in interactive sessions), `PYTHONPATH` entries, the standard library, then `site-packages`.
- It is **not** the operating system `PATH` (which is where the shell looks for executables like `python` or `git`, readable through `os.environ["PATH"]`).
- `sys.path.append("../src")` works but is a hack; prefer installing your project (`pip install -e .`) or running modules with `python -m package.module`.

### 5.3 Command-line arguments and exit codes

```python
import sys
# python report.py 2026-10-01 eu
print(sys.argv)        # ['report.py', '2026-10-01', 'eu']  — all strings; argv[0] is the script
```

| Call | Meaning |
|---|---|
| `sys.argv` | List of command-line arguments (strings) |
| `sys.exit(0)` / `sys.exit()` | Success |
| `sys.exit(1)` (any non-zero int) | Failure — schedulers, CI pipelines, `&&` chains and Airflow/ADF read this |
| `sys.exit("message")` | Prints the message to stderr and exits with code 1 |

`sys.exit` raises `SystemExit`; in a **notebook** it stops the cell with a confusing traceback — raise a normal exception instead. For anything beyond one or two positional arguments use `argparse` (section 6).

### 5.4 Standard streams

| Object | Use |
|---|---|
| `sys.stdout` | Normal output (what `print` writes to) — data, results |
| `sys.stderr` | Errors, warnings, progress — keeps stdout clean for piping: `print("warning", file=sys.stderr)` |
| `sys.stdin` | Read piped input: `for line in sys.stdin:` |
| `sys.stdout.reconfigure(encoding="utf-8")` | Fixes `UnicodeEncodeError` when printing emoji/accents to some Windows consoles |

### 5.5 Less frequent but worth knowing

| Call | Use |
|---|---|
| `sys.exc_info()` | Current exception tuple inside an `except` block (prefer `traceback` / `logging.exception`) |
| `sys.getsizeof(obj)` | Shallow memory size of an object |
| `sys.getrecursionlimit()` / `sys.setrecursionlimit(n)` | Recursion depth (raise carefully) |
| `sys.maxsize` | Largest index-sized int on this platform |
| `sys.flags`, `sys.dont_write_bytecode` | Interpreter flags |

---

## 6. Modern companions: pathlib, shutil, subprocess, argparse, secrets

`os` and `sys` are the foundations; these standard-library modules build on them and are often the better choice.

| Need | Old / low-level | Prefer | Example |
|---|---|---|---|
| Paths | `os.path.join(a, b)` | **`pathlib.Path`** | `Path("data") / "raw" / "sales.csv"`, `.exists()`, `.glob("*.csv")`, `.read_text()`, `.mkdir(parents=True, exist_ok=True)` |
| Copy / move / delete trees | `os.rename`, manual loops | **`shutil`** | `shutil.copy2(src, dst)`, `shutil.move`, `shutil.rmtree(path)`, `shutil.which("git")` |
| Run another program | `os.system("cmd")` | **`subprocess.run`** | `subprocess.run(["git", "status"], capture_output=True, text=True, check=True)` |
| Parse CLI options | `sys.argv[1]` | **`argparse`** | named options, types, `--help` generated for you |
| Generate tokens / API keys | `os.urandom` | **`secrets`** | `secrets.token_urlsafe(32)` |
| Temp files and folders | manual names in `os.getcwd()` | **`tempfile`** | `tempfile.TemporaryDirectory()` |
| Logging to stderr | `print(..., file=sys.stderr)` | **`logging`** | `logging.basicConfig(level=logging.INFO)` |
| Load a local `.env` file | — | `python-dotenv` (third-party) | `load_dotenv()` then `os.getenv(...)` |

Rule of thumb: **read configuration with `os.environ`/`os.getenv`; handle paths with `pathlib`; inspect the interpreter and exit with `sys`; run programs with `subprocess`.**

---

## 7. Seven worked examples

### Example 1 — A typed, validated configuration loader

Why: one place that reads every setting, fails fast with a clear message, and never prints secrets.

```python
import os
from dataclasses import dataclass


def _require(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Required environment variable {name} is missing or empty")
    return value


def _bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    api_base: str
    api_key: str
    timeout: int
    debug: bool

    def __repr__(self) -> str:                       # never leak the key in logs
        return f"Settings(api_base={self.api_base!r}, api_key='***', timeout={self.timeout}, debug={self.debug})"


def load_settings() -> Settings:
    return Settings(
        api_base=_require("API_BASE").rstrip("/"),
        api_key=_require("API_KEY"),
        timeout=int(os.getenv("API_TIMEOUT", "30")),
        debug=_bool("DEBUG"),
    )
```

### Example 2 — Local development with a `.env` file

Why: developers need settings locally without exporting them in every terminal, and without committing them.

```text
# .env  (add ".env" to .gitignore; commit a .env.example with placeholder values instead)
API_BASE=https://api.example.com
API_KEY=replace-me-locally
```

```python
# pip install python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()                    # reads .env into os.environ; does NOT override variables already set
api_base = os.environ["API_BASE"]
```

In production (containers, CI, Fabric/Databricks), variables come from the platform or a vault instead — the code doesn't change, which is exactly the point.

### Example 3 — A well-behaved command-line script (argv, exit codes, stderr)

Why: schedulers, CI and other scripts rely on exit codes; humans rely on `--help`.

```python
import argparse
import os
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Export sales for one region")
    parser.add_argument("region", choices=["eu", "us", "apac"])
    parser.add_argument("--since", default="2026-01-01", help="ISO date")
    parser.add_argument("--out", default=os.path.join("out", "sales.csv"))
    args = parser.parse_args()          # reads sys.argv[1:]

    if not os.getenv("API_KEY"):
        print("error: API_KEY is not set", file=sys.stderr)
        return 2                        # non-zero = failure

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    print(f"exporting {args.region} since {args.since} -> {args.out}", file=sys.stderr)
    # ... call the API and write the file ...
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Run: `python export.py eu --since 2026-09-01`. Check the result in PowerShell with `$LASTEXITCODE`, in bash with `echo $?`.

### Example 4 — Find every CSV in a landing folder, with sizes and dates

Why: the bread and butter of ingestion scripts.

```python
import os
from datetime import datetime

landing = os.getenv("LANDING_DIR", "landing")
for dirpath, dirnames, filenames in os.walk(landing):
    dirnames[:] = [d for d in dirnames if not d.startswith(".")]   # prune hidden folders in place
    for name in filenames:
        if os.path.splitext(name)[1].lower() == ".csv":
            path = os.path.join(dirpath, name)
            size_kb = os.path.getsize(path) / 1024
            modified = datetime.fromtimestamp(os.path.getmtime(path))
            print(f"{path}\t{size_kb:,.1f} KB\t{modified:%Y-%m-%d %H:%M}")
```

`pathlib` equivalent: `for p in Path(landing).rglob("*.csv"): print(p, p.stat().st_size)`.

### Example 5 — An environment "doctor" for debugging

Why: answers "which Python, which venv, which folder, which settings are present?" without revealing secret values.

```python
import os
import sys

REQUIRED = ["API_BASE", "API_KEY", "LANDING_DIR"]

print("Python      :", sys.version.split()[0])
print("Executable  :", sys.executable)
print("Platform    :", sys.platform, "/", os.name)
print("In a venv   :", sys.prefix != sys.base_prefix)
print("Working dir :", os.getcwd())
print("CPU count   :", os.cpu_count())
for name in REQUIRED:
    value = os.getenv(name)
    state = "missing" if value is None else ("EMPTY" if not value.strip() else f"set ({len(value)} chars)")
    print(f"{name:<12}:", state)                 # presence and length only — never the value
print("First 3 sys.path entries:", sys.path[:3])
```

### Example 6 — Safe file writes with `os.replace`

Why: if a job crashes half-way through writing `output.json`, readers must never see a corrupt file.

```python
import json
import os
import tempfile


def write_json_atomically(path: str, data: dict) -> None:
    folder = os.path.dirname(os.path.abspath(path))
    os.makedirs(folder, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=folder, suffix=".tmp")      # same folder => same filesystem
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, path)                                  # atomic swap, overwrites existing
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise
```

### Example 7 — Run another program with a controlled environment

Why: calling `dbt`, `az`, `git` or another script from Python, passing settings without exposing them on the command line.

```python
import os
import subprocess
import sys

child_env = os.environ.copy()
child_env["DBT_TARGET"] = "prod"                        # visible to the child only

result = subprocess.run(
    ["dbt", "build", "--select", "tag:daily"],          # list form: no shell, no injection
    env=child_env, capture_output=True, text=True, check=False,
)
print(result.stdout[-2000:])
if result.returncode != 0:
    print(result.stderr[-2000:], file=sys.stderr)
    sys.exit(result.returncode)
```

If the program isn't installed or isn't on `PATH`, `subprocess.run` raises `FileNotFoundError` before anything runs; check first with `shutil.which("dbt")` or catch the exception.

To run *the same Python* (for example to call pip or another module), use `[sys.executable, "-m", "pip", "install", "x"]`.

---

## 8. Pitfalls and how to avoid them

| Pitfall | What happens | Fix |
|---|---|---|
| `bool(os.getenv("DEBUG"))` | `"false"` is truthy → debug on | Parse explicitly (Example 1) |
| `os.getenv("X", "default")` when `X=""` | You get `""`, not the default | `os.getenv("X") or "default"`, or validate empties |
| `int(os.getenv("PORT"))` when unset | `TypeError: int() ... NoneType` | Give a default string: `int(os.getenv("PORT", "8000"))` |
| Setting `os.environ` and expecting the terminal to see it | The parent shell never changes | Set variables in the shell/platform before launching |
| Relative paths in notebooks/schedulers | `FileNotFoundError` because the working directory differs | Build paths from a configured root or `Path(__file__).parent` |
| `os.chdir` inside functions | Breaks every other relative path in the process | Pass absolute paths instead |
| `os.path.join` for URLs | Backslashes on Windows | String formatting / `urllib.parse.urljoin` |
| `sys.path.append(...)` everywhere | Fragile imports that break when moved | `pip install -e .`, `python -m pkg.module` |
| Confusing `PATH` and `sys.path` | Wrong fix applied | `PATH` = executables (shell); `sys.path` = Python modules |
| `pip install` installs into another Python | `ModuleNotFoundError` | `python -m pip install`, `%pip` in notebooks, check `sys.executable` |
| `os.system(f"... {user_input}")` | Shell injection | `subprocess.run([...])` list form |
| `print(os.environ)` / logging settings objects | Secrets in logs, screenshots, notebook outputs | Print presence/length only (Example 5); custom `__repr__` |
| Passing secrets as CLI arguments (`sys.argv`) | Visible in process lists and shell history | Pass via environment or a vault |
| `sys.exit()` in a notebook | Cell dies with `SystemExit` traceback | Raise an exception |
| `os.remove` / `shutil.rmtree` on a computed path | Deleting the wrong folder | Check the path is inside the expected root first; dry-run print |

---

## 9. Must-master cheat sheet

The 25 calls that cover 95% of real use:

| # | Call | One-line purpose |
|---|---|---|
| 1 | `os.environ["X"]` | Required setting (fails fast) |
| 2 | `os.getenv("X", "d")` | Optional setting with default |
| 3 | `os.environ["X"] = "v"` | Set for this process and its children |
| 4 | `os.environ.copy()` | Build a child process environment |
| 5 | `os.getcwd()` | Where relative paths resolve |
| 6 | `os.path.join(...)` | Build file paths portably |
| 7 | `os.path.exists / isfile / isdir` | Check before reading |
| 8 | `os.path.abspath / dirname / basename / splitext` | Take paths apart |
| 9 | `os.path.getsize / getmtime` | Size and modified time |
| 10 | `os.path.expanduser("~")` | Home directory |
| 11 | `os.listdir / os.scandir` | List a folder |
| 12 | `os.walk(top)` | Recurse through folders |
| 13 | `os.makedirs(p, exist_ok=True)` | Create folders safely |
| 14 | `os.remove(p)` | Delete a file |
| 15 | `os.replace(src, dst)` | Atomic overwrite |
| 16 | `os.cpu_count()` / `os.getpid()` | Sizing and logging |
| 17 | `sys.argv` | Command-line arguments |
| 18 | `sys.exit(code)` | Report success/failure |
| 19 | `sys.executable` | Which Python is running |
| 20 | `sys.version_info` | Version checks |
| 21 | `sys.platform` | OS-specific branches |
| 22 | `sys.path` | Import search path (diagnose, don't hack) |
| 23 | `sys.prefix != sys.base_prefix` | Inside a virtual environment? |
| 24 | `print(..., file=sys.stderr)` | Errors separate from data |
| 25 | `sys.stdout.reconfigure(encoding="utf-8")` | Fix Windows console encoding |

Plus the companions: `pathlib.Path`, `shutil.copy2/rmtree/which`, `subprocess.run([...])`, `argparse`, `secrets.token_urlsafe`, `tempfile`, `logging`.

---

## 10. Practice questions and answers

1. **Do you need `pip install os`?** No — `os` and `sys` are part of the standard library.
2. **What is the difference between `os` and `sys` in one sentence?** `os` talks to the operating system; `sys` talks to the running Python interpreter.
3. **`os.environ["API_KEY"]` vs `os.getenv("API_KEY")` — which for a required secret?** `os.environ[...]` (or `getenv` plus an explicit check) so a missing value fails immediately with a clear error instead of sending `None` to the API.
4. **Why is `DEBUG=false` treated as on by `bool(os.getenv("DEBUG"))`?** Every non-empty string is truthy; parse explicitly.
5. **You set `os.environ["REGION"] = "eu"` in a script. Does your PowerShell window now have `$env:REGION`?** No — only the Python process and its children see it.
6. **A script works from VS Code but fails in Task Scheduler with `FileNotFoundError: config.json`. Likely cause?** Different working directory; build paths from the script's folder or a configured root.
7. **What does `sys.executable` tell you and when is it useful?** The full path of the running interpreter — to diagnose packages installed into a different Python or venv.
8. **What is the difference between `PATH` and `sys.path`?** `PATH` is the OS search path for executables; `sys.path` is Python's search path for modules.
9. **What exit code means success, and why does it matter?** `0`; schedulers, CI and orchestrators use the exit code to mark the run as passed or failed.
10. **Why prefer `subprocess.run(["git", "status"])` over `os.system("git status")`?** No shell injection, captured output, return code and error handling.
11. **How do you overwrite a file safely so readers never see a half-written version?** Write to a temp file in the same folder, then `os.replace(tmp, final)`.
12. **How should a diagnostic script report a secret setting?** Only whether it's present (and maybe its length) — never the value.
13. **What should you use to generate a random API key?** `secrets.token_urlsafe(32)` (not `random`).
14. **How do you check you are inside a virtual environment?** `sys.prefix != sys.base_prefix`.
15. **Why should you not call `sys.exit()` in a notebook?** It raises `SystemExit` and stops the kernel cell awkwardly; raise a normal exception.

Official references: [os](https://docs.python.org/3/library/os.html) · [os.path](https://docs.python.org/3/library/os.path.html) · [sys](https://docs.python.org/3/library/sys.html) · [pathlib](https://docs.python.org/3/library/pathlib.html) · [subprocess](https://docs.python.org/3/library/subprocess.html) · [argparse](https://docs.python.org/3/library/argparse.html) · [secrets](https://docs.python.org/3/library/secrets.html)
