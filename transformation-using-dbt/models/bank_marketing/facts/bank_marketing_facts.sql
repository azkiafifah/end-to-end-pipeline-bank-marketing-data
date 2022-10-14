{{ config(materialized='table') }}

select id 
from {{ ref('dim_loan') }} 
join {{ ref('dim_identification') }}
on dim_loan.id = dim_identification.id