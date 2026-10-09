"""Delete ONE version of a Foundry agent, with safety checks. Dry run unless --yes is given.

Usage (device-code sign-in, same as the other examples):
    python foundry_delete_agent_version.py --version 8            # shows what it would do
    python foundry_delete_agent_version.py --version 8 --yes      # deletes

Refuses to delete the version that live callers get: the one the agent endpoint's
version_selector pins, or the latest version when nothing is pinned. If a selector exists but
no pinned version can be read from it, the script refuses to delete anything. Deletion cannot be undone.
No secrets are used; sign-in is interactive.
"""
import argparse
import json
import os
import sys

TENANT_ID = os.environ.get("TENANT_ID", "30a73c0f-1703-4d60-94f9-d540409677ae")
ENDPOINT = os.environ.get("FOUNDRY_PROJECT_ENDPOINT",
                          "https://jb-pdp-newsletter-eus2.services.ai.azure.com/api/projects/jb-newsletter")
AGENT = os.environ.get("FOUNDRY_AGENT_NAME", "jbnewsletteragentv1")


def protected_versions(agent):
    """Return {version: reason} for versions that must not be deleted."""
    data = agent.as_dict() if hasattr(agent, "as_dict") else dict(agent)
    out = {}
    latest = ((data.get("versions") or {}).get("latest") or {}).get("version")
    selector = (data.get("agent_endpoint") or {}).get("version_selector") or {}

    def walk(node):  # collect every agent_version value inside the selector, whatever its shape
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "agent_version" and v is not None:
                    out[str(v)] = "targeted by the endpoint version_selector"
                walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)
    walk(selector)
    if not out and latest is not None:  # nothing pinned: callers get the latest, so protect it
        out[str(latest)] = "latest version, and nothing else is pinned"
    return out, selector


def main(argv=None, project=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", required=True)
    ap.add_argument("--agent", default=AGENT)
    ap.add_argument("--yes", action="store_true", help="really delete (default is a dry run)")
    args = ap.parse_args(argv)
    version = str(args.version)

    if project is None:
        from azure.ai.projects import AIProjectClient
        from azure.identity import DeviceCodeCredential
        project = AIProjectClient(endpoint=ENDPOINT, credential=DeviceCodeCredential(tenant_id=TENANT_ID))

    existing = [str(v.version) for v in project.agents.list_versions(agent_name=args.agent)]
    print(f"Versions of {args.agent}: {', '.join(existing) or '(none)'}")
    if version not in existing:
        print(f"STOP: version {version} does not exist.")
        return 2

    protected, selector = protected_versions(project.agents.get(agent_name=args.agent))
    print("Endpoint version_selector:", json.dumps(selector) if selector else "(none: latest is served)")
    if selector and not any("selector" in r for r in protected.values()):
        print("STOP: a version_selector exists but I cannot read which version it pins.")
        return 3
    if version in protected:
        print(f"STOP: version {version} is the {protected[version]}. Make another version active first.")
        return 3
    if len(existing) == 1:
        print("STOP: this is the only version.")
        return 3

    if not args.yes:
        print(f"DRY RUN: would delete {args.agent} version {version}. Re-run with --yes to delete.")
        return 0
    result = project.agents.delete_version(agent_name=args.agent, agent_version=version)
    print("Deleted:", getattr(result, "deleted", result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
