-- Template: replace the placeholder before running. This file contains no key.
-- Use the generated assign_public_key.sql from New-FivetranKeys.ps1 instead
-- if you want the public-key body and quoting handled automatically.
USE ROLE ACCOUNTADMIN;
ALTER USER FIVETRAN_USER SET
  RSA_PUBLIC_KEY = 'REPLACE_WITH_PUBLIC_KEY_BODY_WITHOUT_HEADERS_OR_LINE_BREAKS';
DESCRIBE USER FIVETRAN_USER;
-- RSA_PUBLIC_KEY_FP should be populated. Never paste a private key into this SQL.

-- Rotation pattern: register a new public key in the second slot, update
-- Fivetran to the corresponding new private key, then Save & Test and verify sync.
-- ALTER USER FIVETRAN_USER SET RSA_PUBLIC_KEY_2 = 'NEW_PUBLIC_KEY_BODY';
-- After successful verification, retire the OLD first slot:
-- ALTER USER FIVETRAN_USER UNSET RSA_PUBLIC_KEY;
-- Do not remove the slot Fivetran is currently using.
