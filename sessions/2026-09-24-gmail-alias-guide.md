# Gmail alias guide

Date: 2026-09-24 (Australia/Sydney)

## Request

User asked for a clear, reusable GitHub record of how to receive messages sent to `information@fei.com` in the existing `matthieu@frenchexpatsinvestment.com` Gmail inbox. They had performed a similar setup before but did not recall the process.

## Work and reasoning

- Reviewed project memory, the three most recent session notes, repository state, and official Google help.
- Created `EMAIL_ALIAS_GUIDE.md` and linked it from `README.md`.
- Documented the likely Google Workspace approach: add and activate `fei.com` as a secondary domain, then add `information@fei.com` as an alternate email on Matthieu's existing user account. A user alias domain alone mirrors the same local part (`matthieu@fei.com`) and does not produce the requested address.
- Included prerequisite checks, an external delivery test, optional Gmail Send mail as setup, and a fallback when the mailbox is not actually hosted in Google Workspace.
- Updated `MEMORY.md` to point to the guide. No live email account, DNS, or Admin console changes were made; the user's exact hosting arrangement remains unverified.

## Validation and next step

Official Google sources were checked for domain types, user aliases, MX activation, and forwarding. The user can confirm whether their custom-domain inbox is managed in Google Workspace and then follow the matching path in the guide. Review the repository diff and publish the session record and guide under standing authorization.
