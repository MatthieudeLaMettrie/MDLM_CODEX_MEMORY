"""Print current SQL-reference syntax blocks for Cortex AI functions.

This read-only helper does not copy documentation into the repository.
Run with network access: python inspect_ai_function_refs.py
"""

from urllib.request import Request, urlopen
import re

NAMES = (
    "ai_complete", "ai_complete-single-string", "ai_complete-single-file",
    "ai_complete-prompt-object", "ai_complete-structured-outputs",
    "ai_classify", "ai_filter", "ai_agg", "ai_embed",
    "ai_multi_embed", "ai_extract", "ai_sentiment", "ai_summarize",
    "ai_summarize_agg", "ai_similarity", "ai_transcribe", "ai_parse_document",
    "ai_redact", "ai_translate", "ai_count_tokens", "prompt", "to_file",
)

for name in NAMES:
    url = f"https://docs.snowflake.com/en/sql-reference/functions/{name}.md"
    try:
        with urlopen(Request(url, headers={"User-Agent": "SnowPro-study-reference-check/1.0"}), timeout=20) as response:
            body = response.read().decode("utf-8", errors="replace")
        section = re.search(r"^## Syntax\b(.*?)(?=^## |\Z)", body, re.M | re.S)
        syntax = re.search(r"```[^\n]*\n(.*?)```", section.group(1), re.S) if section else None
        if not syntax:
            syntax = re.search(r"```[^\n]*\n(.*?)```", body, re.S)
        snippet = syntax.group(1).strip() if syntax else "No fenced syntax block found"
        print(f"### {name.upper()}\n{url}\n{snippet[:1800]}\n")
    except Exception as exc:
        print(f"### {name.upper()}\n{url}\nERROR {type(exc).__name__}: {exc}\n")
