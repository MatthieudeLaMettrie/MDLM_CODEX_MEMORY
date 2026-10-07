"""Validate authored study assets locally; does not call cloud services.

Standard library checks always run. PyYAML is optional for YAML checks:
  python databricks/validate_materials.py --yaml-library <isolated-PyYAML-directory>
No dependency installation or filesystem mutation is performed by this script.
"""
import argparse
import ast
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--yaml-library", type=Path)
    args = parser.parse_args()
    if args.yaml_library:
        sys.path.insert(0, str(args.yaml_library.resolve()))
    try:
        import yaml
    except ImportError:
        yaml = None
    if yaml:
        class UniqueLoader(yaml.SafeLoader):
            pass

        def unique_mapping(loader, node, deep=False):
            pairs = loader.construct_pairs(node, deep=deep)
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError(f"Duplicate YAML key: {key}")
                result[key] = value
            return result

        UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)

    counts = {"markdown_files": 0, "local_links": 0, "python_files": 0,
              "python_blocks": 0, "yaml_files": 0, "yaml_blocks": 0, "json_files": 0}
    for path in HERE.rglob("*.py"):
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        counts["python_files"] += 1
    for path in HERE.rglob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))
        counts["json_files"] += 1
    for path in HERE.rglob("*.md"):
        counts["markdown_files"] += 1
        text = path.read_text(encoding="utf-8")
        in_fence = False
        language, block = "", []
        plain_lines = []
        for line in text.splitlines():
            if line.startswith("```"):
                if not in_fence:
                    language, block, in_fence = line[3:].strip(), [], True
                else:
                    if language == "python":
                        ast.parse("\n".join(block), filename=f"{path}:python-block")
                        counts["python_blocks"] += 1
                    elif language in {"yaml", "yml"} and yaml:
                        yaml.load("\n".join(block), Loader=UniqueLoader)
                        counts["yaml_blocks"] += 1
                    in_fence = False
            elif in_fence:
                block.append(line)
            else:
                plain_lines.append(line)
        assert not in_fence, f"Unclosed fence: {path}"
        # These authored links use no nested-parenthesis targets or reference links.
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", "\n".join(plain_lines)):
            target = target.strip().strip("<>")
            if re.match(r"[a-zA-Z][\w+.-]*:", target):
                continue
            relative, _, anchor = target.partition("#")
            if relative:
                resolved = (path.parent / unquote(relative)).resolve()
                assert resolved.exists(), f"Missing target: {path} -> {target}"
                counts["local_links"] += 1
            if anchor:
                raise AssertionError(f"Review newly introduced anchor explicitly: {path} -> {target}")
    for pattern in ("*.yml", "*.yaml"):
        for path in HERE.rglob(pattern):
            if yaml:
                yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)
                counts["yaml_files"] += 1

    # Check actual bundle resource references and required task sequencing.
    if yaml:
        resource = HERE / "03_OPERATIONAL_DATA_LAB/bundle/resources/jobs.yml"
        jobs = yaml.load(resource.read_text(encoding="utf-8"), Loader=UniqueLoader)
        job = jobs["resources"]["jobs"]["operational_pipeline"]
        assert job["max_concurrent_runs"] == 1
        tasks = job["tasks"]
        assert [t["task_key"] for t in tasks] == ["bronze", "silver", "gold", "validate"]
        for i, task in enumerate(tasks):
            notebook = (resource.parent / task["notebook_task"]["notebook_path"]).resolve()
            assert notebook.exists(), notebook
            assert task["notebook_task"]["base_parameters"]["stage"] == task["task_key"]
            if i:
                assert task["depends_on"] == [{"task_key": tasks[i - 1]["task_key"]}]
        bundle_path = resource.parent.parent / "databricks.yml"
        bundle = yaml.load(bundle_path.read_text(encoding="utf-8"), Loader=UniqueLoader)
        assert bundle["bundle"]["engine"] == "direct"
        assert list(bundle["targets"]) == ["dev"]
        for relative in bundle["sync"]["paths"]:
            assert (bundle_path.parent / relative).resolve().is_dir()
    practice = (HERE / "07_TROUBLESHOOTING_PRACTICE.md").read_text(encoding="utf-8")
    cases = [int(n) for n in re.findall(r"^### Case (\d+)\b", practice, re.M)]
    assert cases == list(range(1, 29)), cases
    course = (HERE / "02_COURSE_COMPANION.md").read_text(encoding="utf-8")
    lessons = [int(n) for n in re.findall(r"^## Lesson (\d+)\b", course, re.M)]
    assert lessons == list(range(1, 17)), lessons
    for number in range(10):
        assert len(list(HERE.glob(f"{number:02d}_*"))) == 1, number
    print(json.dumps(counts, indent=2))
    print("YAML duplicate-key parsing:", "passed" if yaml else "SKIPPED; install/provide PyYAML")
    print("Local structure/reference checks passed. Cloud/runtime execution is not checked.")


if __name__ == "__main__":
    main()
