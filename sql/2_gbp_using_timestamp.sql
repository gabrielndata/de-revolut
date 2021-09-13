WITH exchange_rate AS
(
	SELECT  from_currency
	       ,rate
	       ,ts
	FROM exchange_rates
	WHERE to_currency = 'GBP' 
) , sum_by_rate_user AS
(
	SELECT  user_id
	       ,currency
	       ,SUM(amount) AS sum_amount
	       ,ts
	FROM transactions
	GROUP BY  user_id
	         ,ts
	         ,currency
)
SELECT  sr.user_id
       ,SUM(sr.sum_amount * coalesce((
SELECT  t.rate
FROM
(
	SELECT  er.rate
	       ,row_number() over (order by er.ts DESC) rn
	FROM exchange_rate er
	WHERE sr.currency = er.from_currency
	AND er.ts <= sr.ts
) t
WHERE t.rn =1) , 1)) AS total_spent_gbp
FROM sum_by_rate_user sr
GROUP BY  sr.user_id
ORDER BY sr.user_id