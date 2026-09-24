# Receive `information@frenchexpatsinvestment.com` in Matthieu's Gmail inbox

The intended setup is:

```text
Someone sends to information@frenchexpatsinvestment.com
              ↓
The message arrives in the existing inbox of
matthieu@frenchexpatsinvestment.com
```

In Google Workspace, `information@frenchexpatsinvestment.com` can be an **email alias** on Matthieu's existing user account. An alias is another address for the same inbox. The original address continues to work, and no second mailbox or domain setup is needed.

## Add the alias in Google Workspace

1. Sign in to the [Google Admin console](https://admin.google.com) with an administrator account that can manage users.
2. Open **Menu → Directory → Users**. You do not need **Account → Domains → Manage domains** for this same-domain address.
3. Open the user `matthieu@frenchexpatsinvestment.com`.
4. Select **Add Alternate Emails** (also called *email aliases* in some views).
5. Enter **`information`** in the alias field. If a domain selector appears, choose **`frenchexpatsinvestment.com`**.
6. Save. Confirm that **`information@frenchexpatsinvestment.com`** appears as an alternate email on Matthieu's user account.

If the address is already assigned to another user, group, or alias, it must be freed before it can be added here. Google says alias changes can take up to 24 hours, though they usually take effect sooner.

## Test it

From an email account outside this Google Workspace account, send a message to `information@frenchexpatsinvestment.com`. Check that it arrives in Matthieu's existing Gmail inbox. Also test the original `matthieu@frenchexpatsinvestment.com` address. If the alias message does not arrive, recheck its spelling and which user owns it in the Admin console.

## Optional: Send replies from the alias

Receiving messages at the alias does not automatically make it the default **From** address. In Matthieu's Gmail, open **Settings → See all settings → Accounts and Import → Send mail as → Add another email address**. Enter `information@frenchexpatsinvestment.com`, follow the confirmation steps, then choose it in the **From** field when writing or replying. You can set it as the default From address if desired. Send a test to an external account to check how the sender appears.

## If this custom-domain address is hosted outside Google Workspace

If you read `matthieu@frenchexpatsinvestment.com` in Gmail but its mail is actually hosted by another provider, create the alias or forwarding address in that provider's control panel instead. Route `information@frenchexpatsinvestment.com` to the existing mailbox there. Gmail's **Forwarding** setting sends mail *out of* Gmail; it does not create a new incoming address for your domain.

## Official reference

- [Google Workspace: add or delete an alternate email address](https://support.google.com/a/answer/33327)
