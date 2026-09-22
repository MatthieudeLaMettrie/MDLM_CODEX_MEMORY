# Session continuity

## Before starting work

1. Read `MEMORY.md` for durable context, decisions, and current priorities.
2. Read the three most recent notes in `sessions/` (or all notes if fewer exist), ordered by the date in their filenames. Follow references to older notes when relevant.
3. Check the working tree and current repository state before editing. Treat notes as context to verify, not as a substitute for current evidence or the user's instructions.

## After substantive work

1. Update `MEMORY.md` with lasting decisions, relevant preferences, current state, and outstanding next steps. Keep it concise; replace stale information rather than accumulating a transcript.
2. Create or update a session note in `sessions/` named `YYYY-MM-DD-short-topic.md`. Use the user's local date and a unique suffix when needed.
3. Record the request, changes, decisions and reasons, validation performed, unresolved issues, and useful next steps. State clearly when an action or check was not completed.
4. Update these records before the final response and include them with related commits when committing is requested. Do not record a commit or push as successful until verified.

Never store passwords, tokens, private keys, or other secrets in continuity files. Preserve unrelated user changes. Commit and push only when authorized by the task.
