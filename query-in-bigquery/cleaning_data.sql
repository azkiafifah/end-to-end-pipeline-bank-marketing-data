CREATE OR REPLACE TABLE `firm-pentameter-363006.bank_marketing.bank_marketing_clean`
cluster by age, job
AS
SELECT ROW_NUMBER() OVER() AS id, age, job, marital, education, defaultloan, housingloan, loan 
FROM `firm-pentameter-363006.bank_marketing.bank_marketing`
where age is not null
and job is not null
and marital is not null
and education is not null
and defaultloan is not null
and housingloan is not null
and loan is not null;