# Flipside Tools

Build and deploy AI agents for blockchain analytics. Query 40+ chains, analyze wallets, track DeFi protocols, and more.

## Install
Mac or Linux users:
```
curl -fsSL https://raw.githubusercontent.com/FlipsideCrypto/flipside-tools/main/install.sh | sh
```
Windows user: Download the latest exe from releases (or use `wsl`)

## Quick Start

**1. Get an API key** from [Flipside](https://flipsidecrypto.xyz/chat/settings/mcp-keys)

**2. Configure the CLI**
```bash
flipside config init
flipside config set apiKey fk_....
```

**3. Verify it works**
```bash
flipside whoami
```

**4. Deploy your first agent**
```bash
flipside agent push examples/defi_analyst.agent.yaml
flipside agent run defi_analyst --message "What's the TVL on Aave?"
```

That's it! You now have a DeFi analyst agent ready to query blockchain data.

---

## Example Agents

Two example agents in [examples/](./examples/):

| Agent | Type | What it does |
|-------|------|--------------|
| `defi_analyst` | chat | Analyze DeFi protocols - TVL, liquidity, DEX volume |
| `top_tokens` | sub | Fetch top tokens by trading volume as structured JSON |

```bash
# Chat agent - natural language
flipside agent run defi_analyst --message "Top DEX protocols by volume this week"

# Sub agent - structured JSON input
flipside agent run top_tokens --data-json '{"chain": "ethereum", "limit": 10}'
```

---

## Build Your Own Agent

### Create a new agent
```bash
flipside agent init my_agent              # Chat agent (conversational)
flipside agent init my_parser --kind sub  # Sub agent (structured I/O)
```

### Edit the YAML file
```yaml
name: my_agent
kind: chat
description: "What this agent does"

systemprompt: |
  You are an expert at... [customize this]

tools:
  - name: run_sql_query    # Query blockchain data
  - name: find_tables      # Discover available tables
  - name: search_web       # Web search for context

maxturns: 10
metadata:
  model: claude-4-5-haiku
```

### Deploy and run
```bash
flipside agent validate my_agent.agent.yaml
flipside agent push my_agent.agent.yaml
flipside agent run my_agent --message "Hello!"
```

---

## Available Tools

Your agents can use these tools:

| Tool | Description |
|------|-------------|
| `run_sql_query` | Execute SQL against 40+ blockchain datasets |
| `find_tables` | Semantic search to discover relevant tables |
| `get_table_schema` | Get column details for a table |
| `search_web` | Search the web for context |
| `get_swap_quote` | Get cross-chain swap quotes |
| `execute_swap` | Execute a cross-chain swap |
| `get_swap_status` | Check swap status |
| `get_swap_tokens` | List available swap tokens |
| `find_workflow` | Find pre-built analysis workflows |
| `publish_html` | Publish visualizations to a public URL |

List all tools: `flipside tools list`

---

## Run SQL Directly

Don't need an agent? Query data directly:

```bash
# Run SQL from command line (saves to data/ folder)
flipside query "SELECT * FROM ethereum.core.fact_blocks LIMIT 5" --output data/blocks.csv

# Run SQL files from queries/ folder
flipside query queries/scrap.sql --output data/scrap.csv

# Run all .sql files in queries folder (bash)
for file in queries/*.sql; do
  filename=$(basename "$file" .sql)
  flipside query "$file" --output "data/${filename}.csv"
done
```

---

## Use Catalog Agents

Flipside maintains pre-built agents you can use immediately:

```bash
# List available agents
flipside catalog agents list

# Run one
flipside catalog agents run data_analyst --message "What's trending in DeFi?"
```

---

## Interactive Chat

Start a REPL for continuous conversation:

```bash
flipside chat repl
```

---

## Stay up to date

Use the built in updater to stay up to date.

```bash
flipside update
```

---

## Command Reference

```bash
# Agents
flipside agent init <name>           # Create new agent
flipside agent validate <file>       # Validate YAML
flipside agent push <file>           # Deploy agent
flipside agent run <name> --message  # Run chat agent
flipside agent run <name> --data-json # Run sub agent
flipside agent list                  # List your agents
flipside agent describe <name>       # View agent details
flipside agent delete <name>         # Delete agent

# Catalog
flipside catalog agents list         # List Flipside agents
flipside catalog agents run <name>   # Run catalog agent

# Tools
flipside tools list                  # List available tools
flipside tools execute <tool> <json> # Execute a tool directly

# Config
flipside config show                 # Show current config
flipside config init                 # Setup wizard
```

### Global Flags

| Flag | Description |
|------|-------------|
| `-j, --json` | Output as JSON (for scripting) |
| `-v, --verbose` | Show request/response details |
| `--api-key` | Override API key for this command |

---

## Troubleshooting

**"API key not found"** → Run `flipside config init`

**"Agent not found"** → Check `flipside agent list` for your agents

**Validation errors** → Run `flipside agent validate <file>` for details

**Debug mode** → Add `-v` flag to see full request/response

---

## Links

- [Flipside Docs](https://docs.flipsidecrypto.xyz)
- [Discord](https://discord.gg/flipside)
- [GitHub Issues](https://github.com/flipsidecrypto/flipside-cli/issues)
