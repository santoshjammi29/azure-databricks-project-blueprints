-- Unity Catalog Zero-Trust Dynamic Masking & Row-Level Security UDFs

-- Dynamic Column Masking for PII Email
CREATE OR REPLACE FUNCTION prod_catalog.security.mask_email(email STRING)
RETURN CASE
  WHEN is_account_group_member('customer_support_leads') THEN email
  ELSE CONCAT(LEFT(email, 2), '****@', SPLIT(email, '@')[1])
END;

-- Dynamic Column Masking for Credit Card PAN
CREATE OR REPLACE FUNCTION prod_catalog.security.mask_pan(pan STRING)
RETURN CASE
  WHEN is_account_group_member('fraud_investigators') THEN pan
  ELSE CONCAT('XXXX-XXXX-XXXX-', RIGHT(pan, 4))
END;

-- Dynamic Row-Level Security for Regional Data Isolation
CREATE OR REPLACE FUNCTION prod_catalog.security.region_rls(region STRING)
RETURN is_account_group_member('global_executives')
  OR is_account_group_member(CONCAT('analyst_region_', LOWER(region)));
