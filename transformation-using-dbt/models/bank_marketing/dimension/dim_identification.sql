{{ config(materialized='table') }}

SELECT
    age,
    job,
    marital,
    education, 
FROM
    {{ ref('bank_marketing_source') }}
GROUP BY
    age, job, marital, education