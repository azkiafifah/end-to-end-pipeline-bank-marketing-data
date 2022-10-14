{{ config(materialized='table') }}

SELECT
    defaultloan,
    housingloan,
    loan, 
FROM
    {{ ref('bank_marketing_source') }}
GROUP BY
    defaultloan, housingloan, loan