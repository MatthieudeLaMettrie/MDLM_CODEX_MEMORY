# Session continuity

## Before starting work

1. Read MEMORY.md for durable context, decisions, and current priorities.
2. Read the three most recent notes in sessions/ (or all notes if fewer exist), ordered by filename date. Follow references to older notes when relevant.
3. Check the working tree and repository state before editing. Verify remembered context against current evidence and the user's instructions.

## Record and publish every session

The user has given standing authorization to record, commit, and push every session in this project, including explanation-only and planning sessions. Do this before each final response so follow-ups are preserved. A later explicit user instruction overrides this default.

1. Create or update a note in sessions/ named YYYY-MM-DD-short-topic.md using Australia/Sydney dates. Continue the same note for the same task; use a unique suffix for separate tasks with colliding names. Include a task identifier when available.
2. Summarize the user's requests, explanations, changes, decisions and reasons, validation, unresolved issues, and next steps. Notes are faithful summaries, not verbatim chat exports. Do not invent unavailable history.
3. Update MEMORY.md when lasting facts, preferences, decisions, current state, or next steps change. Keep it concise and replace stale information. Every session needs a note even when memory needs no change.
4. Review the diff and stage only the session record, relevant memory updates, and task-owned artifacts. Commit and push to the configured remote and current branch without asking again for routine authorization. Honor tool permission requirements.
5. Preserve unrelated user changes. Never force-push, overwrite concurrent work, or change branches merely to publish a note. Reconcile remote updates safely; report unresolved conflicts.
6. Verify the push and report the outcome in the final response. If blocked by authentication, connectivity, permissions, or concurrent edits, preserve the local record and clearly report what remains unpublished.
7. Do not claim an action or check succeeded without evidence. Avoid endless commits just to record the previous commit hash: Git history and the final response provide publication evidence.

Never store passwords, tokens, private keys, or other secrets. Standing authorization applies to this repository's session records and requested artifacts, not unrelated repositories or actions.

These instructions guide tasks running in this repository. They are not a background recorder and cannot guarantee a final write if a task is interrupted or never accesses the project.
