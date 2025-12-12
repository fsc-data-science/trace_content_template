# SQL Style Guide

This document describes the SQL coding style used in this codebase. The style emphasizes simplicity, readability, and consistency for blockchain data analysis queries.

## Core Principles

1. **Simplicity over complexity** - Prefer straightforward queries over elaborate CTEs
2. **Readability** - Code should be easy to understand at a glance
3. **Consistency** - Follow established patterns throughout
4. **Single-purpose queries** - Each query answers one specific question

## Formatting

### Keywords
- Use **lowercase** for SQL keywords: `select`, `from`, `where`, `group by`, `order by`, etc.
- Exception: `SELECT * FROM table LIMIT 5` can use uppercase for exploratory queries
- Use **uppercase** for constants and identifiers when appropriate (e.g., `'BTC'`, `'ETH'`)

### Indentation
- Minimal indentation - keep it simple
- Align `where` clauses with `from`
- Align `and`/`or` conditions under `where`

```sql
select count(1) from ink.core.dim_contracts 
where created_block_timestamp < '2025-11-01'
and created_block_timestamp >= '2025-10-01'
and decimals IS NOT NULL;
```

### Line Breaks
- Break after `select`, `from`, `where`, `group by`, `order by`
- Keep related clauses together
- Use blank lines sparingly, mainly between separate queries

## Query Structure

### Basic Query Pattern
```sql
-- Question as comment
-- Answer as comment above query
select column1, column2
from schema.table
where condition1
and condition2
group by column1
order by column2 desc
limit 1;
```

### Comments
- **Question comments**: Write the question being answered above the query
- **Answer comments**: Place the answer directly above the query with `-- answer`
- **Inline comments**: Use sparingly for clarification, especially for business logic

```sql
-- How many tokens were created on INK in October 2025?
-- 68
select count(1) from ink.core.dim_contracts 
where created_block_timestamp < '2025-11-01'
and created_block_timestamp >= '2025-10-01'
and decimals IS NOT NULL; -- ERC20 requires decimals
```

## Common Patterns

### Counting
- Use `count(1)` instead of `count(*)`
- Use `count(distinct column)` for unique counts

```sql
select count(1) as n_transactions
from ink.core.fact_transactions
where block_timestamp >= '2025-10-01'
and block_timestamp < '2025-11-01';
```

### Date Ranges
- Always use `>= 'start_date'` and `< 'end_date'` pattern (exclusive end)
- Use ISO date format: `'2025-10-01'`
- For single days: `>= '2025-10-15' and < '2025-10-16'`

```sql
where block_timestamp >= '2025-10-01'
and block_timestamp < '2025-11-01'
```

### Top N Queries
- Use `order by column desc` followed by `limit 1` for single answers
- Return the identifier (address, hash, etc.) as the answer

```sql
select from_address, count(1) as n_transactions
from ink.core.fact_transactions
where block_timestamp >= '2025-10-01'
and block_timestamp < '2025-11-01'
group by from_address
order by n_transactions desc
limit 1;
```

### Aggregations
- Use descriptive aliases with underscores: `n_contracts`, `n_eth`, `avg_tx_fee`
- Prefix counts with `n_`: `n_transactions`, `n_blocks`
- Prefix averages with `avg_`: `avg_block_utilization`
- Prefix sums with `sum_` or descriptive names: `total_added`, `net_amount`

### CASE Statements
- Keep CASE statements simple and inline
- Use for conditional aggregations or transformations

```sql
select 
sum(case when to_address = '0x...' then amount else -amount end) as net_amount
from ink.core.ez_native_transfers
where (from_address = '0x...' or to_address = '0x...');
```

### Joins
- Prefer `inner join` written out (not abbreviated)
- Use simple aliases: `lp`, `a`, `c`, `t`
- Place join conditions on the same line or immediately after

```sql
select sum(amount_usd) as n_usd 
from ink.core.ez_token_transfers tt 
inner join crosschain.chain_stats.ez_ink_allowlist c 
  on tt.contract_address = c.token_address
where c.tracks_asset = 'USD'
and block_timestamp >= '2025-10-01'
and block_timestamp < '2025-11-01';
```

## CTEs (Common Table Expressions)

### When to Use
- Use sparingly - prefer direct joins when possible
- Use when logic needs to be reused or when it significantly improves readability
- Use when building queries at granularity for drill-down analysis (see "Granularity for Drill-Down Analysis" section)
- Keep CTEs simple and focused

### CTE Style
- Use lowercase with underscores: `contract_deployers`, `september_contracts`
- End CTEs with commas, final SELECT without comma
- Use descriptive names

```sql
with contract_deployers as (
select distinct i.address as factory_address 
from ink.core.dim_contracts i 
inner join ink.core.dim_contracts i2 on i.address = i2.creator_address 
),

factory_creates as (
select factory_address, count(address) as contract_count
from contract_deployers cd 
left join ink.core.dim_contracts i on cd.factory_address = i.creator_address
and i.created_block_timestamp < '2025-10-01'
and i.created_block_timestamp >= '2025-09-01'
group by factory_address
)

select count(distinct factory_address) from factory_creates;
```

## Naming Conventions

### Table Aliases
- Use short, meaningful aliases: `lp` (liquidity pool), `a` (allowlist), `c` (contracts), `t` (transactions)
- Single letter is acceptable when context is clear

### Column Aliases
- Use lowercase with underscores
- Be descriptive: `n_contracts`, `net_btc_gained`, `avg_tx_fee`
- Prefix patterns:
  - `n_` for counts: `n_transactions`, `n_blocks`
  - `avg_` for averages: `avg_block_utilization`
  - `net_` for net calculations: `net_amount`, `net_btc_gained`

### CTE Names
- Use lowercase with underscores
- Be descriptive: `contract_deployers`, `september_contracts`, `hourly_eth_usd`

## Query Organization

### Section Headers
- Use comment dividers for major sections
- Format: `-- ============================================================================`

```sql
-- ============================================================================
-- CORE SCHEMA TABLES
-- ============================================================================
```

### Table Exploration
- Start each table section with: `SELECT * FROM schema.table LIMIT 5;`
- Follow with questions and queries

### Question Format
- Questions should be specific with defined time ranges
- Questions should have a single calculable answer
- Format: `-- Question text?`

## Granularity for Drill-Down Analysis

### When to Write at Lower Granularity

When answering aggregate questions, consider writing queries **one level of granularity lower** than strictly required. This enables easy drill-down analysis for follow-up questions without rewriting the entire query.

**Use this pattern when:**
- The question asks for a total/sum, but individual components (pools, addresses, contracts) might be interesting
- You anticipate follow-up questions like "which is the top X?" or "are there any outliers?"
- The granular data provides business intelligence value beyond the aggregate

**How to structure:**
1. Build the query at the granular level (e.g., pool-level, address-level) - **only if the number of groupings is small (< 50) such that you could imagine printing the list**
2. Create a final CTE or outer query that aggregates to answer the original question
3. Comment the final aggregation so it can be easily modified or removed for drill-down

**Performance consideration:** If the grouping would result in thousands of rows (e.g., address-level aggregations across many addresses), it may be prudent for speed purposes to aggregate up as soon as needed to answer the question. Reserve granularity for cases where the breakdown is manageable and useful.

```sql
-- what is the total BTC in liquidity pools on Ink as of 2025-11-06 00:00:00.0000?
-- 5.958258284
with btc_tokens as (
select token_address, symbol
from crosschain.chain_stats.ez_ink_allowlist 
where tracks_asset = 'BTC'
),

pool_addresses as (
select distinct pool_address, pool_name 
from ink.defi.ez_dex_liquidity_pool_actions lp
inner join btc_tokens a on lp.token_address = a.token_address
and lp.block_timestamp < '2025-11-06'
and lp.amount > 0
),

inbound_btc as (
select pool_address, pool_name, sum(amount) as n_btc_in
from ink.core.ez_token_transfers 
inner join btc_tokens a on contract_address = a.token_address
inner join pool_addresses p on to_address = p.pool_address
and block_timestamp < '2025-11-06'
group by pool_address, pool_name
), 

outbound_btc as (
select pool_address, pool_name, sum(amount) as n_btc_out
from ink.core.ez_token_transfers 
inner join btc_tokens a on contract_address = a.token_address
inner join pool_addresses p on from_address = p.pool_address
and block_timestamp < '2025-11-06'
group by pool_address, pool_name
),

pool_level_btc_liquidity as (
select pool_address, pool_name,
 n_btc_in, n_btc_out,
sum(n_btc_in) - sum(n_btc_out) as net_btc_in_liquidity 
from inbound_btc full join outbound_btc using (pool_address, pool_name)
group by pool_address, pool_name, n_btc_in, n_btc_out
order by net_btc_in_liquidity desc
)

-- Final aggregation - comment out to see pool-level breakdown
select sum(net_btc_in_liquidity) as total_btc_liquidity 
from pool_level_btc_liquidity;

-- To drill down: replace final select with:
-- select * from pool_level_btc_liquidity;
-- or
-- select * from pool_level_btc_liquidity where net_btc_in_liquidity <= 0.01; -- dead pools
```

**Benefits:**
- Easy to modify for drill-down: comment out final aggregation, add filters
- Enables quick exploration: "top 10 pools", "pools with zero liquidity", etc.
- Reusable CTEs: granular CTEs can be reused in other queries
- Better for exploratory analysis: see distribution, outliers, patterns

**When NOT to use:**
- Simple aggregations where granularity adds no value
- Queries where performance is critical and granularity significantly slows execution
- One-off questions with no anticipated follow-ups
- When the grouping would result in thousands of rows - aggregate up earlier for performance

## Best Practices

1. **Avoid over-engineering** - Simple queries are preferred, but consider granularity for drill-down when valuable
2. **Use direct joins** - Prefer `inner join` in FROM clause over complex CTEs
3. **Filter early** - Put date filters and common conditions in WHERE clause
4. **Single answers** - For "which" questions, return single identifier with `limit 1`
5. **Consistent date patterns** - Always use `>=` and `<` for date ranges
6. **Meaningful aliases** - Use descriptive names that clarify intent
7. **Comment answers** - Always include the answer as a comment above the query
8. **Granularity for exploration** - When writing aggregate queries, consider building at one level lower to enable drill-down analysis

## Anti-Patterns to Avoid

❌ **Don't**: Overuse CTEs when a simple join would suffice
❌ **Don't**: Use inconsistent date range patterns
❌ **Don't**: Create overly complex nested queries
❌ **Don't**: Use vague or unclear aliases
❌ **Don't**: Mix uppercase and lowercase keywords inconsistently
❌ **Don't**: Return multiple rows when a single answer is expected

## Examples

### Good: Simple aggregation
```sql
-- What is the average transaction fee on INK in October 2025?
-- 1.509649095e-7
select avg(tx_fee) as avg_tx_fee
from ink.core.fact_transactions
where block_timestamp >= '2025-10-01'
and block_timestamp < '2025-11-01';
```

### Good: Top N with grouping
```sql
-- Which address sent the most transactions on INK in October 2025?
-- 0xdeaddeaddeaddeaddeaddeaddeaddeaddead0001
select from_address, count(1) as n_transactions
from ink.core.fact_transactions
where block_timestamp >= '2025-10-01'
and block_timestamp < '2025-11-01'
group by from_address
order by n_transactions desc
limit 1;
```

### Good: Conditional aggregation
```sql
-- How much did wrapped ETH supply change on Ink in October 2025?
-- 29794.775297553
select 
sum(case when to_address = '0x4200000000000000000000000000000000000006' 
    then amount else -amount end) as net_amount
from ink.core.ez_native_transfers
where (from_address = '0x4200000000000000000000000000000000000006' 
   or to_address = '0x4200000000000000000000000000000000000006')
and block_timestamp >= '2025-10-01'
and block_timestamp < '2025-11-01';
```

### Good: Simple join
```sql
-- Which BTC liquidity pool on ink gained the most BTC tokens in October 2025?
-- 0xad95f3af523d83f00679764dbefb07ddce15d1e1
select pool_address, pool_name,
sum(case when lower(event_name) in ('mint', 'addliquidity', 'deposit') 
    then amount else -amount end) as net_btc_gained
from ink.defi.ez_dex_liquidity_pool_actions lp
inner join crosschain.chain_stats.ez_ink_allowlist a 
  on lp.token_address = a.token_address
where a.tracks_asset = 'BTC'
and lp.block_timestamp >= '2025-10-01'
and lp.block_timestamp < '2025-11-01'
and lp.amount > 0
group by pool_address, pool_name
order by net_btc_gained desc
limit 1;
```

### Good: Granularity for drill-down
```sql
-- what is the total BTC in liquidity pools on Ink as of 2025-11-06 00:00:00.0000?
-- 5.958258284
with btc_tokens as (
select token_address, symbol
from crosschain.chain_stats.ez_ink_allowlist 
where tracks_asset = 'BTC'
),

pool_addresses as (
select distinct pool_address, pool_name 
from ink.defi.ez_dex_liquidity_pool_actions lp
inner join btc_tokens a on lp.token_address = a.token_address
and lp.block_timestamp < '2025-11-06'
and lp.amount > 0
),

inbound_btc as (
select pool_address, pool_name, sum(amount) as n_btc_in
from ink.core.ez_token_transfers 
inner join btc_tokens a on contract_address = a.token_address
inner join pool_addresses p on to_address = p.pool_address
and block_timestamp < '2025-11-06'
group by pool_address, pool_name
), 

outbound_btc as (
select pool_address, pool_name, sum(amount) as n_btc_out
from ink.core.ez_token_transfers 
inner join btc_tokens a on contract_address = a.token_address
inner join pool_addresses p on from_address = p.pool_address
and block_timestamp < '2025-11-06'
group by pool_address, pool_name
),

pool_level_btc_liquidity as (
select pool_address, pool_name,
 n_btc_in, n_btc_out,
sum(n_btc_in) - sum(n_btc_out) as net_btc_in_liquidity 
from inbound_btc full join outbound_btc using (pool_address, pool_name)
group by pool_address, pool_name, n_btc_in, n_btc_out
order by net_btc_in_liquidity desc
)

-- Final aggregation - comment out to see pool-level breakdown
select sum(net_btc_in_liquidity) as total_btc_liquidity 
from pool_level_btc_liquidity;
```

