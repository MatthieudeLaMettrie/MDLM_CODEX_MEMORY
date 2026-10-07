"""Inventory official Snowflake AI/ML Markdown pages without copying their content.

Run with network access: python build_ai_ml_doc_atlas.py
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path
import re
import sys
import time
from urllib.request import Request, urlopen


ROOTS = [
    ("Snowflake Cortex", "https://docs.snowflake.com/en/user-guide/snowflake-cortex/llms.txt"),
    ("Snowflake CoCo", "https://docs.snowflake.com/en/user-guide/cortex-code/llms.txt"),
    ("Snowflake ML", "https://docs.snowflake.com/en/developer-guide/snowflake-ml/llms.txt"),
]
BROWSE_ROOTS = {
    ROOTS[0][1]: "https://docs.snowflake.com/en/guides-overview-ai-features",
    ROOTS[1][1]: "https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code",
    ROOTS[2][1]: "https://docs.snowflake.com/en/developer-guide/snowflake-ml/overview",
}
EXTRAS = [
    (
        "AI/ML overview and ML Functions",
        "https://docs.snowflake.com/en/guides-overview-ai-features.md",
        [
            ("Snowflake AI and ML", "https://docs.snowflake.com/en/guides-overview-ai-features.md"),
            ("ML Functions", "https://docs.snowflake.com/en/guides-overview-ml-functions.md"),
            ("Anomaly Detection", "https://docs.snowflake.com/en/user-guide/ml-functions/anomaly-detection.md"),
            ("Classification", "https://docs.snowflake.com/en/user-guide/ml-functions/classification.md"),
            ("Forecasting", "https://docs.snowflake.com/en/user-guide/ml-functions/forecasting.md"),
            ("Top Insights", "https://docs.snowflake.com/en/user-guide/ml-functions/top-insights.md"),
            ("Time-series preprocessing", "https://docs.snowflake.com/en/user-guide/ml-functions/preprocessing.md"),
        ],
    ),
    (
        "SQL AI Function references",
        "https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql.md",
        [
            (name.upper(), f"https://docs.snowflake.com/en/sql-reference/functions/{name}.md")
            for name in (
                "ai_complete", "ai_complete-single-string", "ai_complete-single-file",
                "ai_complete-prompt-object", "ai_complete-structured-outputs",
                "ai_classify", "ai_filter", "ai_agg", "ai_embed", "ai_multi_embed",
                "ai_extract", "ai_sentiment", "ai_summarize", "ai_summarize_agg",
                "ai_similarity", "ai_transcribe", "ai_parse_document", "ai_redact",
                "ai_translate", "ai_count_tokens", "prompt", "to_file",
            )
        ],
    ),
]
LINK = re.compile(r"^- \[([^]]+)\]\((https://docs\.snowflake\.com/[^)]+)\)$", re.M)
HEADING = re.compile(r"^##? (.+)$", re.M)
OUTPUT = Path(__file__).with_name("07_AI_ML_DOC_ATLAS.md")
DOC_LINK = re.compile(r"(?<=\]\()(https://docs\.snowflake\.com/[^)]+)(?=\))")


def browser_url(source_url: str) -> str:
    """Turn Snowflake's machine-readable source URL into a reader-facing page URL."""
    if source_url in BROWSE_ROOTS:
        return BROWSE_ROOTS[source_url]
    if source_url.endswith(".md"):
        return source_url[:-3]
    return source_url


def rewrite_existing_links() -> None:
    """Fix links in the saved inventory without re-fetching hundreds of source pages."""
    content = OUTPUT.read_text(encoding="utf-8")
    content = DOC_LINK.sub(lambda match: browser_url(match.group(1)), content)
    content = content.replace("[Official section index]", "[Browse Snowflake documentation]")
    content = content.replace(
        "The first three sections come from live official section indexes; the final two add ML Function and SQL reference pages linked by the user's entry points. Run `python build_ai_ml_doc_atlas.py` to refresh.",
        "The first three sections come from live official section indexes; the final two add ML Function and SQL reference pages linked by the user's entry points. The table links open normal documentation pages; the `llms.txt` and `.md` URLs are used only to build the inventory. Run `python build_ai_ml_doc_atlas.py` to refresh.",
    )
    OUTPUT.write_text(content, encoding="utf-8")
    print(f"Rewrote reader-facing links in {OUTPUT} without re-fetching pages")


def fetch(url: str) -> str:
    for attempt in range(3):
        try:
            request = Request(url, headers={"User-Agent": "SnowPro-study-doc-inventory/1.0"})
            with urlopen(request, timeout=25) as response:
                return response.read().decode("utf-8", errors="replace")
        except Exception:
            if attempt == 2:
                raise
            time.sleep(0.5 * (attempt + 1))
    raise AssertionError("unreachable")


def summarize(url: str) -> tuple[str, list[str], str | None]:
    try:
        content = fetch(url)
        headings = [re.sub(r"[#*`\[\]]", "", h).strip() for h in HEADING.findall(content)]
        return url, headings[:4], None
    except Exception as exc:
        return url, [], f"{type(exc).__name__}: {exc}"


def cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def main() -> None:
    groups: list[tuple[str, str, list[tuple[str, str]]]] = []
    for group, index_url in ROOTS:
        entries = LINK.findall(fetch(index_url))
        if not entries:
            raise RuntimeError(f"No documentation links parsed from {index_url}")
        groups.append((group, index_url, entries))
    groups.extend(EXTRAS)

    urls = sorted({url for _, _, entries in groups for _, url in entries})
    metadata: dict[str, tuple[list[str], str | None]] = {}
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(summarize, url) for url in urls]
        for future in as_completed(futures):
            url, headings, error = future.result()
            metadata[url] = (headings, error)

    lines = [
        "# Snowflake AI/ML documentation atlas",
        "",
        f"Generated {date.today().isoformat()} from Snowflake's official `llms.txt` section indexes.",
        "This is a **page inventory**, not a claim that every page is examined in depth or that every detail is on the GES-C02 exam.",
        "Each entry was fetched to check availability and read its Markdown headings. Use the [deep-dive guide](04_AI_ML_DEEP_DIVE.md) for the synthesized study notes.",
        "The first three sections come from live official section indexes; the final two add ML Function and SQL reference pages linked by the user's entry points. The table links open normal documentation pages; the `llms.txt` and `.md` URLs are used only to build the inventory. Run `python build_ai_ml_doc_atlas.py` to refresh.",
        "",
        "| Collection | Indexed pages |",
        "| --- | ---: |",
    ]
    lines += [f"| [{group}]({browser_url(index_url)}) | {len(entries)} |" for group, index_url, entries in groups]
    lines += ["", f"Unique pages: **{len(urls)}**. Fetch failures: **{sum(bool(v[1]) for v in metadata.values())}**.", ""]
    for group, index_url, entries in groups:
        lines += [f"## {group}", "", f"[Browse Snowflake documentation]({browser_url(index_url)})", "", "| Page | First section headings | Fetch |", "| --- | --- | --- |"]
        for title, url in entries:
            headings, error = metadata[url]
            status = "OK" if error is None else f"Error: {cell(error)}"
            lines.append(f"| [{cell(title)}]({browser_url(url)}) | {cell('; '.join(headings[:3]))} | {status} |")
        lines.append("")
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(urls)} unique pages; {sum(bool(v[1]) for v in metadata.values())} fetch failures")


if __name__ == "__main__":
    if sys.argv[1:] == ["--rewrite-links"]:
        rewrite_existing_links()
    elif len(sys.argv) == 1:
        main()
    else:
        raise SystemExit("Usage: python build_ai_ml_doc_atlas.py [--rewrite-links]")
