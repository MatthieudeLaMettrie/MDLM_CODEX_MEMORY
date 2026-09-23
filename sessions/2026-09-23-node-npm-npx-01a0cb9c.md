# Node.js, npm and npx explained

Date: 2026-09-23 Australia/Sydney
Task: 01a0cb9c-aeca-7080-b993-eece2b0cf008

The user requested a beginner-friendly explanation of supplied text about Node.js, npm and npx. Explain runtime as the program that executes JavaScript, package as reusable code or a tool, and dependency as a package a project needs. Node runs JavaScript outside browsers, npm manages project packages and scripts, and npx invokes commands supplied by packages.

Illustrative commands: node app.js runs a user's file; npm install express adds a server library; npx prettier --check . runs a formatter's checking command. Examples are explanatory and were not executed or installed. Explain local versus global installation and package.json's dependency list.

Corrections: npx can reuse project dependencies or install missing packages into npm's cache. It does not require global installation, but does not mean no download, no disk storage, or no lasting effects from the command. It does not always select the newest version. Modern npx uses npm exec; npm also runs commands and scripts. Server-side means executing on the server handling requests, while Node also supports local scripts and development tools.

Verified with official documentation:
- https://nodejs.org/en/learn/getting-started/introduction-to-nodejs
- https://docs.npmjs.com/about-npm/
- https://docs.npmjs.com/cli/v11/commands/npx/

Read MEMORY.md, AGENTS.md and the three most recent notes. Initial working tree clean, detached HEAD e954db4 matching the cached origin/main. Initial fetch was denied access to Git metadata; retry with authorized elevated execution before publication. No lasting preference or project decision changed, so MEMORY.md remains unchanged. Documentation-only work; review diff and whitespace, then commit and normal push HEAD to origin/main under standing authorization. No branch switch or force push. Git history and final response establish publication outcome.

## Follow-up: HTML study guide

User requested an HTML study guide, an explanation of runtime, and additional environments/runtimes for executing .js and .py files. Created RUNTIME_STUDY_GUIDE.html, linked it from README.md and recorded its location in memory. Self-contained responsive document with print styling, source links, execution flow, terminology, Node/npm/npx roles and corrections, runtime tables, scenario selector, practice commands, troubleshooting and a five-question quiz with feedback/reset.

Coverage includes browser JavaScript engines, Node, Deno, Bun, cloud environments; CPython, PyPy, Jupyter kernels, Pyodide, MicroPython/CircuitPython and containers. Distinguishes editors, shells, runtimes, engines, package managers, infrastructure and interpreter selection. Python -m does not download missing packages; npx can cache installations. Official Node/npm/MDN/Deno/Bun/Python/PyPy/Jupyter/Pyodide/MicroPython/CircuitPython/PyPA documentation informed the guide.

Validation: HTML parser confirmed tag nesting/closure. Node VM with minimal DOM stubs validated script execution, all five scenario branches, quiz empty/all-correct/all-wrong scoring, reset and print-handler dispatch. Unique IDs and internal anchor targets checked. This is logic verification, not browser rendering validation. Browser preview of the local file was explicitly blocked by browser URL security policy; no workaround attempted. Responsive and print CSS are implemented but not visually verified. No example package installations performed. Initial follow-up worktree clean at 017c99e. Review diff/whitespace and publish task-owned files under standing authorization; Git history and final response establish publication result.
