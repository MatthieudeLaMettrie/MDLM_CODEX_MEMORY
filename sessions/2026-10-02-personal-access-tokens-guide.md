# Personal Access Tokens study guide

User requested another study-series part on PAT, described as programmatic access token, covering what/how/why. Added guides/api/PERSONAL_ACCESS_TOKENS_GUIDE.md as Part 3 and linked from README and Parts 1/2. Clarified common expansion Personal Access Token and its programmatic use.

Covers direct provider credential versus Bearer/Basic transport, owner/resource/scope/expiry checks, reasons to use it, OAuth/application/managed-identity alternatives, GitHub fine-grained token setup and read-only contents request, Azure DevOps Basic build-read and GitLab PRIVATE-TOKEN examples, Databricks workspace/scoped tokens and OAuth preference, vault storage, replacement/revocation, troubleshooting and quiz.

Current official GitHub, Microsoft and GitLab documentation checked. Python snippets compile without execution, guide links/anchors/fences and Git whitespace checked. No PATs created, read from environment/vault, tested, rotated or revoked; no external API requests executed except public documentation reads. Public-resource success explicitly does not prove private-resource authorization. Session and durable architecture also recorded in AGY memory.
