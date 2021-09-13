explain (analyze,buffers)
WITH union_table AS
(
	SELECT  ts
	       ,user_id
	       ,currency AS from_currency
	       ,amount
	       ,NULL     AS rate
	FROM transactions
	UNION ALL
	SELECT  ts
	       ,null AS user_id
	       ,from_currency
	       ,0    AS amount
	       ,rate
	FROM exchange_rates
	WHERE to_currency = 'GBP' 
), g_rate AS
(
	SELECT  *
	       ,SUM(case WHEN rate is not null THEN 1 end) over (partition by from_currency ORDER BY ts) AS grp_close
	FROM union_table
), final_table as (
SELECT  *
       ,first_value(rate) over (partition by from_currency, grp_close ORDER BY ts, user_id NULLS FIRST) AS last_rate
FROM g_rate
ORDER BY from_currency, ts)
select user_id, sum(amount * coalesce(last_rate, 1)) as total_spent_gbp
from final_table
where user_id is not NULL
group by user_id
order by user_id