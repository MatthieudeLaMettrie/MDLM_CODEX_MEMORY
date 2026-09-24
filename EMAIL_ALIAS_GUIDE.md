# Receive `information@fei.com` in the existing Gmail inbox

This guide is for the desired setup:

```text
Someone sends to information@fei.com
              ↓
Google Workspace delivers it to the inbox of
matthieu@frenchexpatsinvestment.com
```

The new address is an **email alias**. It is an extra receiving address for the same mailbox, not a separate inbox or a change to the account's sign-in address. Mail sent to the old address continues to arrive there too.

## Before starting

- Confirm that `matthieu@frenchexpatsinvestment.com` is managed in **Google Workspace** and that you have access to [admin.google.com](https://admin.google.com) with permission to manage domains and users. Gmail's ordinary inbox settings cannot create this cross-domain Workspace alias.
- Own and control the DNS settings for `fei.com`. If another mail provider currently receives `@fei.com` mail, plan its migration before changing MX records; changing them affects the entire domain.
- Check whether `fei.com` is already in the same Google Workspace account under **Account → Domains → Manage domains**. If it is, skip the domain-add step below. If it belongs to another Workspace account, resolve that first.
- Check whether `information@fei.com` is already used by a user, group, or alias. An address cannot be assigned twice.

## Step 1: Add and activate `fei.com` (if needed)

1. Sign in to [Google Admin console](https://admin.google.com) as an administrator.
2. Open **Menu → Account → Domains → Manage domains → Add a domain**.
3. Enter `fei.com` and choose **Secondary domain**. This is the appropriate Admin console route when the new address has a different name before `@` (`information`, rather than `matthieu`). A **user alias domain** automatically gives users the *same* name at the second domain; by itself, it would create `matthieu@fei.com`, not `information@fei.com`.
4. Follow Google's prompts to verify ownership of `fei.com`, usually by adding a DNS record at the domain's DNS host.
5. In **Manage domains**, activate Gmail for `fei.com` and set its MX records as Google currently instructs. Follow the values shown in your Admin console or [Google's MX setup guide](https://support.google.com/a/answer/87127). Allow time for DNS changes to take effect.

Adding the secondary domain does **not** require creating another paid user/mailbox for this alias. Do not create `information@fei.com` as a separate user if the aim is delivery to Matthieu's existing inbox.

## Step 2: Add the exact address to Matthieu's account

1. In [Google Admin console](https://admin.google.com), open **Menu → Directory → Users**.
2. Open the user `matthieu@frenchexpatsinvestment.com`.
3. Select **Add Alternate Emails** (the interface may also call these *email aliases*).
4. Enter `information` as the name before `@` and select **`fei.com`** as the domain.
5. Save. Google says alias changes can take up to 24 hours, though they are usually quicker.

The finished alias should appear as `information@fei.com` on **Matthieu's** user account. Keep the original user account active.

## Step 3: Test delivery

From an external email account, send one message to `information@fei.com` and another to `matthieu@frenchexpatsinvestment.com`. Check that **both** appear in Matthieu's existing Gmail inbox. If the new-address test fails, confirm the alias spelling, domain verification, Gmail activation, and `fei.com` MX records. DNS changes can take up to 72 hours to propagate.

## Optional: Reply from `information@fei.com`

Receiving at an alias does not necessarily make it the default **From** address for replies. In Matthieu's Gmail, open **Settings → See all settings → Accounts and Import → Send mail as → Add another email address**. Add `information@fei.com`, follow the confirmation prompts, and select it in the **From** field when composing. You can set it as the default From address if desired. Send a test reply to an external account and inspect the displayed sender and reply-to address.

## If this is ordinary Gmail rather than Google Workspace

If `matthieu@frenchexpatsinvestment.com` is merely being read inside a personal `@gmail.com` account, the Admin console steps above do not apply. Create `information@fei.com` with the provider that handles mail for `fei.com`, then configure that provider to **forward** messages to `matthieu@frenchexpatsinvestment.com`; use Gmail's **Send mail as** setting separately if you want to reply from the new address. The exact forwarding controls depend on that provider. Gmail's own forwarding setting sends mail **out of** the Gmail account, so it is not the setting for routing `information@fei.com` into it.

## Official references

- [Google Workspace: add a user alias domain or secondary domain](https://support.google.com/a/answer/7502379)
- [Google Workspace: add an alternate email address to a user](https://support.google.com/a/answer/33327)
- [Google Workspace: set up MX records](https://support.google.com/a/answer/87127)
- [Gmail: automatic forwarding](https://support.google.com/mail/answer/10957)
