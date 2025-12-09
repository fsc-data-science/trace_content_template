# Quick Start for Humans

Copy and paste the below into your LLM:

---

**Explain this TRACE content template repository, confirm the Flipside MCP tools are available, and if they work, run this quick test query. Then suggest an example analysis I could perform.**

**Test Query (should be fast):**
```sql
select max(block_timestamp) from ethereum.core.fact_blocks;
```

**Example analysis prompt:**
```
Distribution of tx counts by block on ethereum over last 24 hours
```

**If MCP tools are not available, alert me immediately.**

---