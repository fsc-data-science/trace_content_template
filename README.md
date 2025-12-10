# TRACE Content Template

This repository serves as a template for creating new TRACE analysis content repositories.
Timestamped Reproducible Analytics for Crypto Ecosystems.

## Purpose

Each TRACE analysis should be its own independent git repository, cloned from this template. This ensures:
- **Reproducibility**: Each analysis is self-contained with its own queries, data, and results
- **Version Control**: Independent versioning and history per analysis
- **Sharing**: Easy to share, cite, or embed individual analyses
- **Separation**: Analysis content separate from website infrastructure

## Prerequisites

Before starting, ensure you have:

1. **UV (Python package manager)** — Install with:
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **FlipsideAI MCP Key** — Required for running SQL queries via the Flipside MCP tools to query crypto data. Available at: https://flipsidecrypto.xyz/chat/settings/mcp-keys - generous free tier available. 

3. **Verify installation**:
   ```bash
   uv run python --version
   ```

4. **Read the guides**:
   - `templates.md` — Report layout options
   - `highcharts_embedding_guide.md` — Chart conventions
   - `GET-STARTED.md` - An LLM input to explain the repo and confirm your MCP key is active.

---

## Quick Start

### 1. Create a New Analysis Repository

CLONE & RENAME is easiest way.

```bash
# Clone this template
git clone <template-repo-url> my-analysis-name
cd my-analysis-name

# Remove template git history and initialize new repo
rm -rf .git
git init
git add .
git commit -m "Initial commit: Analysis template"
```

### 2. Choose a Template

Review `templates.md` and select the appropriate layout:

| Template | Best For |
|----------|----------|
| **0: Minimal** | Single visualization with evolving data |
| **1: Simple Overview** | Standard report with metrics + viz + table |
| **2: Comparison** | Comparing two groups side-by-side |
| **3: Alternating Narrative** | Deep-dive with multiple advanced metrics |
| **4: Multi-Section Report** | Linear narrative, static/time-bound analysis |
| **5: Grid Dashboard** | Multiple self-explanatory visualizations |
| **6: Viz + Table** | Minimalist with summary statistics |
| **7: Report Style** | Multi-faceted overview at consistent depth |

### 3. Create Your Files

1. **Create `REPORT.html`** following your chosen template structure
2. **Add SQL queries** → `queries/` folder (e.g., `01_market_share.sql`)
3. **Add data files** → `data/` folder (e.g., `01_market_share.json`)
4. **Add visual files** → `visuals/` folder (e.g., `AREA_market_share.html`)
5. **Create `trace-metadata.json`** with your analysis details

### 4. Commit and Push

```bash
git add .
git commit -m "Initial analysis"
git remote add origin <your-repo-url>
git push -u origin main
```

---

## Directory Structure

```
my-analysis-repo/
├── trace-metadata.json          # REQUIRED: Metadata for TRACE website
├── templates.md                 # Report layout templates (choose one)
├── REPORT.html                  # Final report (embeds visuals into chosen template layout)
├── README.md                    # Analysis-specific README
├── pyproject.toml               # UV project configuration
├── highcharts_embedding_guide.md # Highcharts style guide
├── queries/                     # SQL query files
│   ├── 01_market_share.sql
│   └── 02_volume_analysis.sql
├── data/                        # JSON data files (match query names)
│   ├── 01_market_share.json
│   └── 02_volume_analysis.json
├── visuals/                     # Standalone Highcharts HTML files (viewable individually)
│   ├── AREA_market_share.html   # Complete HTML with data embedded
│   └── LINE_volume_daily.html
├── utils/
│   └── swap_placeholder.py      # Placeholder replacement utility
└── assets/
    └── thumbnail.png
```

## File Relationships

- **QUERY → DATA**: 1:1 relationship
  - `queries/01_market_share.sql` → `data/01_market_share.json`

- **DATA → VISUAL**: 1:many relationship  
  - `data/01_market_share.json` → `visuals/AREA_market_share.html`
  - `data/01_market_share.json` → `visuals/LINE_market_share.html`

### VISUALS vs REPORT

| File | Purpose | Contains |
|------|---------|----------|
| `visuals/*.html` | **Standalone** — viewable in browser for debugging/review | Complete HTML (`<html>`, `<head>`, Highcharts CDN, data embedded) |
| `REPORT.html` | **Final deliverable** — the published analysis | Full report with charts duplicated from `visuals/` |

**Why duplication?** Each VISUAL file is self-contained so you can open it directly to test/debug a single chart. The REPORT then assembles all visuals into the final narrative layout.

> ⚠️ **Keep in sync**: If you edit a chart in REPORT, update the matching VISUAL file (and vice versa). They should always match.

---

## Assembly Process

This section documents how to rebuild the REPORT from component files **without re-running SQL queries**.

### Step 1: Create HTML Structure

Create `REPORT.html` following your chosen template layout from `templates.md`. Use placeholders for content that will be injected:

```html
<script>
  const data01 = {{DATA_01_PLACEHOLDER}};
</script>

<details class="query-section">
  <summary>View SQL Query</summary>
  <pre><code class="sql">{{QUERY_01_PLACEHOLDER}}</code></pre>
</details>

<div class="chart-wrapper">
  {{VISUAL_01_PLACEHOLDER}}
</div>
```

### Step 2: Inject Content with swap_placeholder.py

Use the utility to replace placeholders with file contents:

```bash
# Inject data into REPORT
uv run python utils/swap_placeholder.py REPORT.html "{{DATA_01_PLACEHOLDER}}" data/01_market_share.json

# Inject data in STANDALONE VISUAL
uv run python utils/swap_placeholder.py visuals/AREA_market_share.html "{{VISUAL_01_PLACEHOLDER}}" data/01_market_share.json
```

### Step 3: Validate

Run the validation script to catch common issues:

```bash
uv run python utils/validation.py --verbose
```

### Step 4: Finalize

1. Ensure all CSS is inlined in `<style>` tags (standalone report)
2. Ensure Highcharts loads via CDN
3. Update metadata sections (Author, Reviewer, Network(s), Timestamp Range)
4. Test that the report renders correctly with no broken references


---

## Highcharts Best Practices

See `highcharts_embedding_guide.md` for complete documentation. Key rules:

1. **Use built-in `format:` strings** — avoid custom `formatter: function()`
2. **Colors**: Use the high-contrast palette (`#0000B9`, `#FF2424`, etc.)
3. **Credits**: Set to `'Data: FlipsideAI'`
4. **Smart Titles & Subtitles** The title should be the point, the subtitle defining key terms or adding context.
5. **X-axis dates**: Use `{value:%b '%y}` format (e.g., "Jan '20")

---

## `trace-metadata.json` Format

**CRITICAL**: Every content repository MUST include this file.

```json
{
  "analysis": {
    "id": "aerodrome-rise",
    "title": "The Rise of Aerodrome DEX on Base",
    "subtitle": "Market dominance analysis from August 2023 to August 2024",
    "htmlFile": "aerodrome-rise.html"
  },
  "repository": {
    "url": "https://github.com/username/trace-aerodrome-rise",
    "branch": "main"
  },
  "metadata": {
    "author": "Your Name",
    "reviewer": "Reviewer Name",
    "networks": ["Base"],
    "timestampRange": {
      "start": "2023-08-01",
      "end": "2024-08-31"
    },
    "analysisDate": "2025-11-20",
    "dataSource": "FlipsideAI"
  }
}
```

### Field Descriptions

#### `analysis` (required)
- `id`: Unique identifier (used in URLs, no spaces/special chars)
- `title`: Display title for the analysis
- `subtitle`: Brief description shown on landing page
- `htmlFile`: Path to the final HTML file (relative to repo root)
- `thumbnail`: Optional thumbnail image path

#### `repository` (required)
- `url`: Full GitHub/GitLab URL to the repository
- `branch`: Branch name (usually "main")

#### `metadata` (required)
- `author`: Analysis author name
- `reviewer`: Optional reviewer name
- `networks`: Array of blockchain networks analyzed
- `timestampRange`: Object with `start` and `end` dates (YYYY-MM-DD)
- `analysisDate`: When the analysis was completed (YYYY-MM-DD)
- `dataSource`: Data provider (e.g., "FlipsideAI")

---

## Validation

### Automated Validation

Run the validation script to catch common issues:

```bash
# Basic validation
uv run python utils/validation.py

# Verbose output with all details
uv run python utils/validation.py --verbose

# Custom thresholds
uv run python utils/validation.py --min-data-size 500 --check-sync
```

The script checks:
- ✅ Required directories exist (`data/`, `queries/`, `visuals/`)
- ✅ Files exist with correct extensions
- ✅ Files meet minimum size thresholds (catches truncation)
- ✅ `REPORT.html` exists
- ✅ `trace-metadata.json` is valid and not using placeholder values
- ✅ No unresolved `{{PLACEHOLDER}}` patterns
- ✅ Data content appears embedded in REPORT and visuals (sync check)

### Manual Checklist

After automated validation passes:

- [ ] VISUAL files match REPORT (keep in sync!)
- [ ] TOC updated and links work
- [ ] Report is standalone (no broken external references)
- [ ] Highcharts loads and renders correctly
- [ ] Credits show "Data: FlipsideAI"
- [ ] Colors follow `highcharts_embedding_guide.md` palette
- [ ] No custom formatter functions (use `format:` strings)

---

## TRACE Website Integration

The TRACE website will:

1. **Scan repositories** for `trace-metadata.json` files
2. **Extract metadata** to build landing page cards
3. **Link to HTML files** via GitHub raw content URL
4. **Provide links** to the GitHub repository for queries/data

### Raw Content URL Format

```
https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{htmlFile}
```

### HTML File Requirements

- Must be self-contained (all CSS inlined)
- Highcharts via CDN
- All data embedded in HTML
- Include link back to GitHub repository

---

## Best Practices

1. **Keep it simple**: Static HTML, no build process
2. **Self-contained**: Analysis works when cloned standalone
3. **Document everything**: Methodology, data sources, assumptions
4. **Version your data**: Commit data files to git
5. **Tag releases**: Use git tags for major versions
6. **Validate JSON**: Ensure `trace-metadata.json` is valid before committing

---

## Example Repository

**[eth_fusaka](https://github.com/fsc-data-science/eth_fusaka)** — Median Ethereum Transaction Fees analysis with key upgrade milestones (2020–present)

Demonstrates:
- Proper README structure
- `trace-metadata.json` configuration
- Query → Data → Visual file relationships
- Final REPORT.html with embedded Highcharts

---

## Questions?

See the main [TRACE website repository](https://github.com/fsc-data-science/TRACE) for integration details.
