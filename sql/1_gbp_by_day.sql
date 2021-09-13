WITH largest_exchange_rate AS
(
	SELECT  from_currency
	       ,rate
	       ,row_number() over (partition by from_currency,to_currency ORDER BY ts DESC ) rn
	FROM exchange_rates
	WHERE to_currency = 'GBP'
) , sum_by_rate_user AS
(
	SELECT  user_id
	       ,currency
	       ,SUM(amount) AS sum_amount
	FROM transactions
	GROUP BY  user_id
	         ,currency
)
SELECT  user_id
       ,sum(sum_amount*coalesce(fr.rate,1)) AS sum_CBP_amount
FROM sum_by_rate_user sr
LEFT JOIN
(
	SELECT  from_currency
	       ,rate
	FROM largest_exchange_rate
	WHERE rn=1
) fr
ON sr.currency = fr.from_currency
group by user_id
order by user_id