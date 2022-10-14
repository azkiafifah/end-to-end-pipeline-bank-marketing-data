EXPORT DATA
  OPTIONS (
    uri = 'gs://wfwijaya-fellowship/data/*.csv',
    format = 'CSV',
    overwrite = true,
    header = true,
    field_delimiter = ',')
AS (
  SELECT *
  FROM `firm-pentameter-363006.bank_marketing.bank_marketing_clean`
  ORDER BY age
);