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

## Choose the sender in Outlook

These steps use the full alias recorded in this guide, `information@frenchexpatsinvestment.com`. If you actually created `info@frenchexpatsinvestment.com`, use that exact address instead.

1. First complete the **Send mail as** setup in Gmail above. Google requires that custom From address to be added and confirmed before using it with **Google Workspace Sync for Microsoft Outlook (GWSMO)**.
2. In Outlook, start a new message or reply. Look for **From** above the **To** field. If it is hidden, in **classic Outlook** select **Options → From**; in **new Outlook** select **Options → Show From**.
3. If you use **GWSMO**, select `matthieu@frenchexpatsinvestment.com` or `information@frenchexpatsinvestment.com` in **From**. Google says you can send from a verified alias in Outlook with GWSMO. If the alias is not listed, try entering the full address in the From field, then send a test message to an external account. Do not assume a reply will automatically choose the address to which the incoming message was sent.
4. Check the received test message's **From** and **Reply-To** addresses. If they show Matthieu's primary address when you chose the alias, review the Gmail Send mail as setup and your Outlook connection type.

If Outlook is connected to Gmail as a standard Google/IMAP account instead of GWSMO, Microsoft's **From** menu normally selects an *account*, and a Workspace alias is not a separate account. Simply creating a receiving alias in Google Admin does not guarantee an Outlook sender choice. Microsoft's and Google's help pages do not document a universal alias-sending procedure for every Outlook/Gmail connection type. In that case, use Gmail's verified **From** selector for reliable alias sending, or confirm the supported Outlook setup with your Workspace administrator. Do not add the alias as a separate mailbox unless it has its own login.

## If this custom-domain address is hosted outside Google Workspace

If you read `matthieu@frenchexpatsinvestment.com` in Gmail but its mail is actually hosted by another provider, create the alias or forwarding address in that provider's control panel instead. Route `information@frenchexpatsinvestment.com` to the existing mailbox there. Gmail's **Forwarding** setting sends mail *out of* Gmail; it does not create a new incoming address for your domain.

## Official reference

- [Google Workspace: add or delete an alternate email address](https://support.google.com/a/answer/33327)
- [Google Workspace: work with messages in Outlook using GWSMO](https://support.google.com/a/users/answer/158095)
- [Gmail: send emails from a different address or alias](https://support.google.com/mail/answer/22370)
- [Microsoft: change the account used to send email in Outlook](https://support.microsoft.com/en-us/outlook/change-the-account-used-to-send-email-messages)
