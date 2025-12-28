-- Sample SQL Queries for Customer Balance History Analysis
-- Generated from customer_balance_history.csv

-- ============================================================================
-- Query 1: Balance for specific customers on a specific date
-- ============================================================================
-- Question: "What was the Thrive Cash balance for customers 23306353 and 16161481 on 2023-03-21?"

-- Method 1: Using window function (most efficient)
WITH ranked_balances AS (
    SELECT 
        customer_id,
        transaction_date,
        current_balance,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id 
            ORDER BY transaction_date DESC
        ) as rn
    FROM customer_balance_history
    WHERE customer_id IN ('23306353', '16161481')
      AND transaction_date <= '2023-03-21'
)
SELECT 
    customer_id,
    transaction_date as balance_as_of_date,
    current_balance as thrive_cash_balance
FROM ranked_balances
WHERE rn = 1
ORDER BY customer_id;

-- ============================================================================
-- EXPECTED OUTPUT for Query 1
-- ============================================================================
-- customer_id | balance_as_of_date      | thrive_cash_balance
-- ------------+-------------------------+--------------------
-- 16161481    | 2023-03-20 15:30:00     | 45.50
-- 23306353    | 2023-03-21 10:15:00     | 120.00
--
-- Note: The balance shown is as of the last transaction on or before 2023-03-21

-- ====================================================
-- Additional Queries for Finance Team
-- ==================================================== 
-- ============================================================================
-- Query 2: Current balance for specific customers
-- ============================================================================
-- Question: "What is the current Thrive Cash balance for customers 23306353 and 16161481?"

SELECT 
    customer_id,
    current_balance as thrive_cash_balance,
    cumulative_earned,
    cumulative_spent,
    cumulative_expired
FROM customer_current_balances
WHERE customer_id IN ('23306353', '16161481')
ORDER BY customer_id;


-- ============================================================================
-- Query 3: Balance history for a customer over time
-- ============================================================================
-- Question: "Show me the complete balance history for customer 23306353"

SELECT 
    customer_id,
    transaction_date,
    transaction_id,
    transaction_type,
    transaction_amount,
    cumulative_earned,
    cumulative_spent,
    cumulative_expired,
    current_balance
FROM customer_balance_history
WHERE customer_id = '23306353'
ORDER BY transaction_date;


-- ============================================================================
-- Query 4: Balance at end of each month
-- ============================================================================
-- Question: "What was the balance at the end of each month for customer 23306353?"

WITH monthly_balances AS (
    SELECT 
        customer_id,
        DATE_TRUNC('month', transaction_date) as month,
        transaction_date,
        current_balance,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id, DATE_TRUNC('month', transaction_date)
            ORDER BY transaction_date DESC
        ) as rn
    FROM customer_balance_history
    WHERE customer_id = '23306353'
)
SELECT 
    customer_id,
    month,
    transaction_date as last_transaction_date,
    current_balance as month_end_balance
FROM monthly_balances
WHERE rn = 1
ORDER BY month;


-- ============================================================================
-- Query 5: Customers with balance above threshold on specific date
-- ============================================================================
-- Question: "Which customers had a balance > $100 on 2023-03-21?"

WITH balances_on_date AS (
    SELECT 
        customer_id,
        transaction_date,
        current_balance,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id 
            ORDER BY transaction_date DESC
        ) as rn
    FROM customer_balance_history
    WHERE transaction_date <= '2023-03-21'
)
SELECT 
    customer_id,
    transaction_date as balance_as_of_date,
    current_balance
FROM balances_on_date
WHERE rn = 1
  AND current_balance > 100
ORDER BY current_balance DESC;


-- ============================================================================
-- Query 6: Balance change between two dates
-- ============================================================================
-- Question: "How much did customer 23306353's balance change between 2023-01-01 and 2023-03-21?"

WITH balance_start AS (
    SELECT 
        customer_id,
        current_balance as start_balance
    FROM customer_balance_history
    WHERE customer_id = '23306353'
      AND transaction_date <= '2023-01-01'
    ORDER BY transaction_date DESC
    LIMIT 1
),
balance_end AS (
    SELECT 
        customer_id,
        current_balance as end_balance
    FROM customer_balance_history
    WHERE customer_id = '23306353'
      AND transaction_date <= '2023-03-21'
    ORDER BY transaction_date DESC
    LIMIT 1
)
SELECT 
    bs.customer_id,
    bs.start_balance,
    be.end_balance,
    (be.end_balance - bs.start_balance) as balance_change,
    ROUND(((be.end_balance - bs.start_balance) / NULLIF(bs.start_balance, 0) * 100), 2) as pct_change
FROM balance_start bs
JOIN balance_end be ON bs.customer_id = be.customer_id;


-- ============================================================================
-- Query 7: Top 10 customers by balance on specific date
-- ============================================================================
-- Question: "Who were the top 10 customers by balance on 2023-03-21?"

WITH balances_on_date AS (
    SELECT 
        customer_id,
        transaction_date,
        current_balance,
        cumulative_earned,
        cumulative_spent,
        cumulative_expired,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id 
            ORDER BY transaction_date DESC
        ) as rn
    FROM customer_balance_history
    WHERE transaction_date <= '2023-03-21'
)
SELECT 
    customer_id,
    transaction_date as balance_as_of_date,
    current_balance,
    cumulative_earned,
    cumulative_spent,
    cumulative_expired
FROM balances_on_date
WHERE rn = 1
ORDER BY current_balance DESC
LIMIT 10;


-- ============================================================================
-- Query 8: Customers with zero balance on specific date
-- ============================================================================
-- Question: "Which customers had a zero balance on 2023-03-21?"

WITH balances_on_date AS (
    SELECT 
        customer_id,
        transaction_date,
        current_balance,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id 
            ORDER BY transaction_date DESC
        ) as rn
    FROM customer_balance_history
    WHERE transaction_date <= '2023-03-21'
)
SELECT 
    customer_id,
    transaction_date as balance_as_of_date,
    current_balance
FROM balances_on_date
WHERE rn = 1
  AND current_balance = 0
ORDER BY customer_id;


-- ============================================================================
-- Query 9: Average balance across all customers on specific date
-- ============================================================================
-- Question: "What was the average Thrive Cash balance across all customers on 2023-03-21?"

WITH balances_on_date AS (
    SELECT 
        customer_id,
        current_balance,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id 
            ORDER BY transaction_date DESC
        ) as rn
    FROM customer_balance_history
    WHERE transaction_date <= '2023-03-21'
)
SELECT 
    COUNT(DISTINCT customer_id) as total_customers,
    ROUND(AVG(current_balance), 2) as avg_balance,
    ROUND(MIN(current_balance), 2) as min_balance,
    ROUND(MAX(current_balance), 2) as max_balance,
    ROUND(SUM(current_balance), 2) as total_balance
FROM balances_on_date
WHERE rn = 1;


-- ============================================================================
-- Query 10: Transactions that affected balance on specific date
-- ============================================================================
-- Question: "What transactions occurred on 2023-03-21 for customer 23306353?"

SELECT 
    customer_id,
    transaction_date,
    transaction_id,
    transaction_type,
    transaction_amount,
    current_balance as balance_after_transaction
FROM customer_balance_history
WHERE customer_id = '23306353'
  AND DATE(transaction_date) = '2023-03-21'
ORDER BY transaction_date;


-- ============================================================================
-- Query 11: Balance trend over time (daily snapshots)
-- ============================================================================
-- Question: "Show daily balance snapshots for customer 23306353 in March 2023"

WITH daily_balances AS (
    SELECT 
        customer_id,
        DATE(transaction_date) as date,
        MAX(transaction_date) as last_transaction_time,
        current_balance,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id, DATE(transaction_date)
            ORDER BY transaction_date DESC
        ) as rn
    FROM customer_balance_history
    WHERE customer_id = '23306353'
      AND transaction_date >= '2023-03-01'
      AND transaction_date < '2023-04-01'
)
SELECT 
    customer_id,
    date,
    last_transaction_time,
    current_balance
FROM daily_balances
WHERE rn = 1
ORDER BY date;


-- ============================================================================
-- Query 12: Customers who never spent their Thrive Cash
-- ============================================================================
-- Question: "Which customers have earned Thrive Cash but never spent or expired any?"

SELECT 
    customer_id,
    current_balance,
    cumulative_earned,
    cumulative_spent,
    cumulative_expired
FROM customer_current_balances
WHERE cumulative_spent = 0
  AND cumulative_expired = 0
  AND cumulative_earned > 0
ORDER BY cumulative_earned DESC;
