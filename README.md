# Task
The goal of this home task is to assess the candidate’s code style, problem solving methodology, and command of various skill sets.

# SQL CHALLENGE
Please see http://sqlfiddle.com/#!17/3ff32 or
https://dbfiddle.uk/?rdbms=postgres_9.6&fiddle=6eeee53c62aef4e84720cf4074a81e9a for
database schema.
Given the transactions table and table containing exchange rates. Exchange rate timestamps are rounded to second, transactions are rounded up to millisecond. We have only data for one day, 1st of April, 2018. Please note there are no exchange rate from GBP to GBP as it is always 1

1. Write down a query that gives us a breakdown of spend in GBP by each user. Use the
exchange rate with the largest timestamp.
2. (If you consider yourself senior) Write down the same query, but this time, use the latest exchange rate smaller or equal than the transaction timestamp. Solution  should have the two columns: user_id, total_spent_gbp, ordered by user_id
3. Bonus for postgres superstars: Consider same schema, but now let’s add some random data, to simulate real scale: http://sqlfiddle.com/#!17/c6a70 or https://dbfiddle.uk/?rdbms=postgres_9.6&fiddle=231257838892f0198c58bb5f46fb0d5d Write a solution for the previous task. Please ensure It executes within 5 seconds.

## SQL SOLUTION
###  1. Write down a query that gives us a breakdown of spend in GBP by each user. Use the exchange rate with the largest timestamp.
```sql
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
```

###  2. (If you consider yourself senior) Write down the same query, but this time, use the latest exchange rate smaller or equal than the transaction timestamp. Solution  hould have the two columns: user_id, total_spent_gbp, ordered by user_id
```sql
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
```

### 3. Bonus for postgres superstars: Consider same schema, but now let’s add some random data, to simulate real scale: http://sqlfiddle.com/#!17/c6a70 or https:// bfiddle.uk/?rdbms=postgres_9.6&fiddle=231257838892f0198c58bb5f46fb0d5d Write a solution for the previous task. Please ensure It executes within 5 seconds.
```sql
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
```

# PYTHON CHALLENGE
The program must have the following:
1. Full solution written in Python 3.6
2. In case you are using any third-party variables, a requirements.txt files should be
specified
3. Programs should get input from stdin and print results to stdout.
4. Any debugging or logging information should be printed to stderr
5. Use argparse, to specify parameters. --help should print out usage instructions.
6. Unit tests are a must.
7. Filename specified in the task description

**Task 1:**

Given an input as json array (each element is a flat dictionary) write a program that will parse
this json, and return a nested dictionary of dictionaries of arrays, with keys specified in
command line arguments and the leaf values as arrays of flat dictionaries matching appropriate
groups

**python nest.py nesting_level_1 nesting_level_2 ... nesting_level_n**

Example input for json can be found here: http://jsonformatter.org/74f158
When invoked like this:

**cat input.json | python nest.py currency country city**

The output should be something like this: http://jsonformatter.org/615048
Please note that the nesting keys should be stripped out from the dictionaries in the leaves.
Also please note that the program should support an arbitrary number of arguments, that is
arbitrary level of nesting.

**Task 2:**

Create a REST service from the first task. Make sure your methods support basic auth.
*Api authentication User: admin, password: admin*

# Solution

## CLI usage
```bash
cat input.json | python nest.py nesting_level_1 nesting_level_2 ... nesting_level_n
# or 
python nest.py nesting_level_1 nesting_level_2 ... nesting_level_n

#example
cat input.json | python nest.py currency country city
python nest.py import.json currency country city
```

## API usage
```bash
cd /path/to/nest_json
docker-compose up
```
# Recommend the usage of postman for step bellow
``` curl
curl --location --request POST 'http://localhost:5000/api/v1/nestify?group_by=currency,country,city' \
--user admin:admin \
--header 'Content-Type: application/json' \
--data-raw '[
  {
    "country": "US",
    "city": "Boston",
    "currency": "USD",
    "amount": 100
  },
  {
    "country": "FR",
    "city": "Paris",
    "currency": "EUR",
    "amount": 20
  },
  {
    "country": "FR",
    "city": "Lyon",
    "currency": "EUR",
    "amount": 11.4
  },
  {
    "country": "ES",
    "city": "Madrid",
    "currency": "EUR",
    "amount": 8.9
  },
  {
    "country": "UK",
    "city": "London",
    "currency": "GBP",
    "amount": 12.2
  },
  {
    "country": "UK",
    "city": "York",
    "currency": "FBP",
    "amount": 10.9
  },
  {
    "country": "US",
    "city": "Boston",
    "currency": "USD",
    "amount": 100
  },
  {
    "country": "FR",
    "city": "Paris",
    "currency": "EUR",
    "amount": 20
  },
  {
    "country": "FR",
    "city": "Lyon",
    "currency": "EUR",
    "amount": 11.4
  },
  {
    "country": "ES",
    "city": "Madrid",
    "currency": "EUR",
    "amount": 8.9
  },
  {
    "country": "UK",
    "city": "York",
    "currency": "GBP",
    "amount": 12.2
  },
  {
    "country": "UK",
    "city": "Manchester",
    "currency": "FBP",
    "amount": 10.9
  },
  {
    "country": "US",
    "city": "Boston",
    "currency": "USD",
    "amount": 100
  },
  {
    "country": "FR",
    "city": "Paris",
    "currency": "EUR",
    "amount": 20
  },
  {
    "country": "FR",
    "city": "Lyon",
    "currency": "EUR",
    "amount": 11.4
  },
  {
    "country": "ES",
    "city": "Madrid",
    "currency": "EUR",
    "amount": 8.9
  },
  {
    "country": "UK",
    "city": "Lancaster",
    "currency": "GBP",
    "amount": 12.2
  },
  {
    "country": "UK",
    "city": "London",
    "currency": "FBP",
    "amount": 10.9
  },
  {
    "country": "US",
    "city": "Boston",
    "currency": "USD",
    "amount": 100
  },
  {
    "country": "FR",
    "city": "Paris",
    "currency": "EUR",
    "amount": 20
  },
  {
    "country": "FR",
    "city": "Lyon",
    "currency": "EUR",
    "amount": 11.4
  },
  {
    "country": "ES",
    "city": "Madrid",
    "currency": "EUR",
    "amount": 8.9
  },
  {
    "country": "UK",
    "city": "London",
    "currency": "GBP",
    "amount": 30.0
  },
  {
    "country": "UK",
    "city": "London",
    "currency": "FBP",
    "amount": 20.9
  },
  {
    "country": "US",
    "city": "Boston",
    "currency": "USD",
    "amount": 100
  },
  {
    "country": "FR",
    "city": "Paris",
    "currency": "EUR",
    "amount": 20
  },
  {
    "country": "FR",
    "city": "Lyon",
    "currency": "EUR",
    "amount": 11.4
  },
  {
    "country": "ES",
    "city": "Madrid",
    "currency": "EUR",
    "amount": 8.9
  },
  {
    "country": "UK",
    "city": "London",
    "currency": "GBP",
    "amount": 12.2
  },
  {
    "country": "UK",
    "city": "London",
    "currency": "FBP",
    "amount": 10.9
  },
  {
    "country": "US",
    "city": "Boston",
    "currency": "USD",
    "amount": 100
  },
  {
    "country": "FR",
    "city": "Paris",
    "currency": "EUR",
    "amount": 20
  },
  {
    "country": "FR",
    "city": "Lyon",
    "currency": "EUR",
    "amount": 11.4
  },
  {
    "country": "ES",
    "city": "Madrid",
    "currency": "EUR",
    "amount": 8.9
  },
  {
    "country": "UK",
    "city": "London",
    "currency": "GBP",
    "amount": 12.2
  },
  {
    "country": "UK",
    "city": "London",
    "currency": "FBP",
    "amount": 10.9
  }
]'
```

## Test
```bash
cd /path/to/nest_json
docker-compose -f docker-compose-test.yml run revolut_nest_app
```

### Example

INPUT 

````json
[
  {
    "country": "US",
    "city": "Boston",
    "currency": "USD",
    "amount": 100
  },
  {
    "country": "FR",
    "city": "Paris",
    "currency": "EUR",
    "amount": 20
  },
  {
    "country": "FR",
    "city": "Lyon",
    "currency": "EUR",
    "amount": 11.4
  },
  {
    "country": "ES",
    "city": "Madrid",
    "currency": "EUR",
    "amount": 8.9
  },
  {
    "country": "UK",
    "city": "London",
    "currency": "GBP",
    "amount": 12.2
  },
  {
    "country": "UK",
    "city": "London",
    "currency": "FBP",
    "amount": 10.9
  }
]
````

OUTPUT
```json
{
  "EUR": {
    "ES": {
      "Madrid": [
        {
          "amount": 8.9
        }
      ]
    },
    "FR": {
      "Lyon": [
        {
          "amount": 11.4
        }
      ],
      "Paris": [
        {
          "amount": 20
        }
      ]
    }
  },
  "FBP": {
    "UK": {
      "London": [
        {
          "amount": 10.9
        }
      ]
    }
  },
  "GBP": {
    "UK": {
      "London": [
        {
          "amount": 12.2
        }
      ]
    }
  },
  "USD": {
    "US": {
      "Boston": [
        {
          "amount": 100
        }
      ]
    }
  }
}
```

# Final Considerations
* SQL challenge
  * In the third SQL challenge I managed to achieve a processing time of less than 900 ms without changing the DB schema using a union approach instead of the traditional join approach.
  * My first approach was simple and intuitive, using join as a base, when performing the third challenge to reduce execution time I was able to initially still using join reduce the time from 38 seconds to 10 seconds when modifying to lateral cross join, but it wasn't enough to achieve the desired result, that's why I modified the initial strategy getting higher performance by reducing the number of loops. I used EXPLAIN ANALYZE to find the biggest runtime offender.
* The Python challenge
  * As a data engineer I am more used to pyspark than to python itself, so I usually face some challenge when I have to leave this api completely and go back to the main language.
  * I used the internet to find resources that helped me to finish this challenge, projects with a lot of similarity such as https://github.com/arkataev/nest_json.
  * As a security recommendation, I would never use basic auth as an authentication method, thus resorting to more secure market practices.
  * I would recommend using BDD, as behavior-oriented testing increases the transparency of the process and makes it easier to understand.