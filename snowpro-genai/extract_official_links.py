"""Extract official Snowflake links from a supplied C02 study-guide PDF.

Usage: python extract_official_links.py path/to/SnowProGenAIStudyGuideC02.pdf
Requires pypdf. Writes 06_OFFICIAL_DOC_INDEX.md beside this script.
"""

from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit
import sys

from pypdf import PdfReader


def section(page: int) -> str | None:
    if page == 7:
        return "Domain 1: Snowflake for Gen AI overview"
    if page in (9, 10):
        return "Domain 2: Snowflake Gen AI functions"
    if page == 12:
        return "Domain 3: governance"
    if page == 13:
        return "Domain 4: document processing"
    return None


def label(url: str) -> str:
    parts = urlsplit(url).path.strip("/").split("/")
    tail = " / ".join(parts[-2:])
    return tail.replace("-", " ").replace("_", " ") or urlsplit(url).netloc


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Pass the local SnowProGenAIStudyGuideC02.pdf path")
    pdf = Path(sys.argv[1])
    groups: dict[str, set[str]] = defaultdict(set)
    for number, page in enumerate(PdfReader(str(pdf)).pages, 1):
        heading = section(number)
        if heading is None:
            continue
        for annotation_ref in page.get("/Annots", []):
            action = annotation_ref.get_object().get("/A", {})
            uri = action.get("/URI")
            if not uri:
                continue
            url = str(uri)
            host = urlsplit(url).netloc.lower()
            if host in ("docs.snowflake.com", "docs.snowflake.cn", "quickstarts.snowflake.com") or host.endswith(".snowflake.com"):
                groups[heading].add(url)

    parts = [
        "# Official Snowflake resource links from the C02 PDF",
        "",
        "Extracted from the official study-guide PDF dated 2026-04-30.",
        "These are the distinct official Snowflake documentation, developer-guide, quickstart, and Snowflake-authored reading URLs embedded in its four domain resource pages, grouped by PDF page. Some pages redirect, change, or become legacy; extraction does **not** mean every linked page was individually validated in this study pass. The main [study guide](01_STUDY_GUIDE.md) cites the pages checked for its specific claims. Third-party reading assets are omitted.",
        "",
        "The complete Snowflake documentation catalog is much larger than this exam scope. Use this list as the official guide's reading map, and recheck live pages at exam time.",
        "",
    ]
    count = 0
    for heading in (
        "Domain 1: Snowflake for Gen AI overview",
        "Domain 2: Snowflake Gen AI functions",
        "Domain 3: governance",
        "Domain 4: document processing",
    ):
        urls = sorted(groups[heading])
        count += len(urls)
        parts.extend([f"## {heading} ({len(urls)} links)", ""])
        parts.extend(f"- [{label(url)}]({url})" for url in urls)
        parts.append("")
    parts.insert(2, f"{count} domain-link entries across the four PDF resource sections (duplicates across domains retained).")
    parts.insert(3, "")
    output = Path(__file__).with_name("06_OFFICIAL_DOC_INDEX.md")
    output.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {output} ({count} entries)")


if __name__ == "__main__":
    main()
