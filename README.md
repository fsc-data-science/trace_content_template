# TRACE Content Template

This repository serves as a template for creating new TRACE analysis content repositories.

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

2. **FlipsideAI MCP Key** — Required for running SQL queries via the Flipside MCP tools

3. **Verify installation**:
   ```bash
   uv run python --version
   ```

## Quick Start

### 1. Create a New Analysis Repository

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

### 2. Customize the Template

1. **Rename `content-template.html`** to `REPORT.html` (or your analysis name, e.g., `aerodrome-rise.html`)
   - This file becomes your final standalone HTML report
   
2. **Update the HTML content**:
   - Replace title, subtitle, and all lorem ipsum text
   - Replace `REPLACE_WITH_GITHUB_REPO_URL` with your actual GitHub repository URL (in navigation and footer links)
   - Add your Highcharts visualizations
   - Add your data tables
   - Update the Table of Contents
   - Fill in Author, Reviewer, Network(s), Timestamp Range, Data source

3. **Add your analysis files**:
   - SQL queries → `queries/` folder
   - Data files → `data/` folder
   - Visual files → `visuals/` folder (see `highcharts_embedding_guide.md` for chart configuration)

4. **Create `trace-metadata.json`** (copy from `trace-metadata.json.example`)

5. **Update this README.md** with your analysis details:
   - Replace the template description with your analysis overview
   - Add key findings / summary
   - Document your specific repository structure
   - Include data sources and methodology
   - Add rebuild instructions specific to your analysis
   - Keep an "About TRACE" section linking back to this template

### 3. Create `trace-metadata.json`

**CRITICAL**: Every content repository MUST include a `trace-metadata.json` file in the root directory. This file tells the TRACE website how to link to and display your analysis.

Copy `trace-metadata.json.example` to `trace-metadata.json` and fill in your analysis details.

## Directory Structure

```
my-analysis-repo/
├── trace-metadata.json          # REQUIRED: Metadata for TRACE website
├── content-template.html        # Rename this to your analysis name
├── REPORT.html                  # Final standalone HTML report (generated)
├── INSTRUCTIONS.md              # Guide for rebuilding REPORT from components
├── README.md                    # Analysis-specific README
├── pyproject.toml               # UV project configuration
├── highcharts_embedding_guide.md # Highcharts style guide and patterns
├── queries/                     # SQL query files (01_*.sql, 02_*.sql, ...)
│   ├── 01_market-share.sql
│   ├── 02_whale-transactions.sql
│   └── 03_pool-analysis.sql
├── data/                        # Data files (JSON, matches query names)
│   ├── 01_market-share.json
│   ├── 02_whale-transactions.json
│   └── 03_pool-analysis.json
├── visuals/                      # Highcharts HTML visual files (VIZTYPE_TITLE.html)
│   ├── AREA_market_share_weekly.html
│   └── LINE_volume_daily.html
├── utils/                        # Utility scripts
│   └── swap_placeholder.py      # Placeholder replacement for report assembly
└── assets/                      # Images, thumbnails
    └── thumbnail.png
```

## Workflow & File Organization

### Generation Process

Analyses are typically generated via LLM/MCP calls with access to Python, terminal, JavaScript, etc. The process outputs:

- **REPORT**: Final standalone HTML file (e.g., `aerodrome-rise.html`)
- **DATA**: JSON files in `data/` folder, one per query
- **QUERY**: SQL files in `queries/` folder, one per data file
- **VISUAL**: Highcharts HTML files in `visuals/` folder
- **METADATA**: `trace-metadata.json` with analysis metadata
- **INSTRUCTIONS**: Documentation for rebuilding the report (see below)

**Build Utility**:
A Python utility `utils/swap_placeholder.py` is provided to help assemble the final report. It replaces text placeholders (e.g., `{{DATA_01}}`) with the contents of a file.

**Python Setup**:
This repository uses [UV](https://github.com/astral-sh/uv) for Python environment management. Install UV, then run Python scripts:

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run Python scripts with UV
uv run python utils/swap_placeholder.py my-report.html "{{DATA_01}}" data/01_data.json
```

UV will automatically install Python and manage the virtual environment.

### File Naming Conventions

- **QUERY files**: Use sequential prefixes for ordering (e.g., `01_market_share.sql`, `02_whale_transactions.sql`)
- **DATA files**: Match query names (e.g., `01_market_share.json`, `02_whale_transactions.json`)
- **VISUAL files**: Use descriptive names with chart type prefix (e.g., `AREA_tx_fee_revenue_usd_weekly.html`, `LINE_daily_volume.html`)

### File Relationships

- **1 QUERY = 1 DATA**: Each SQL query produces exactly one data file (1:1 relationship)
- **1 DATA = 1+ VISUAL**: Each data file can be visualized by one or more visual files (1:many relationship)
- **REPORT embeds everything**: The final HTML report should be standalone, with all data, visuals, and query text embedded/injected

### INSTRUCTIONS File

The `INSTRUCTIONS.md` file (or section in README) documents how to rebuild the report from the component files. This is **guidance for future LLM/human rebuilders**, not necessarily a fully automated script.

**Purpose**: Document the assembly process so a future LLM can reconstruct the report without re-running queries.

**Expected content**:
- File structure and relationships
- Mapping of QUERY → DATA → VISUAL files
- Step-by-step assembly process
- Where/how to inject each component into the REPORT template
- Any conventions or patterns used

**Note**: Some duplication is expected. Highcharts configuration will appear in both:
- Individual VISUAL files (standalone for review/debugging)
- Final REPORT file (embedded for self-contained report)

This duplication is acceptable and keeps both files self-contained.

## `trace-metadata.json` Format

Create a `trace-metadata.json` file in the root of your repository with the following structure:

```json
{
  "analysis": {
    "id": "aerodrome-rise",
    "title": "The Rise of Aerodrome DEX on Base",
    "subtitle": "Market dominance analysis from August 2023 to August 2024",
    "htmlFile": "aerodrome-rise.html",
    "thumbnail": "assets/thumbnail.png"
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
- `branch`: Branch name (usually "main" or "master")

#### `metadata` (required)
- `author`: Analysis author name
- `reviewer`: Optional reviewer name
- `networks`: Array of blockchain networks analyzed
- `timestampRange`: Object with `start` and `end` dates (YYYY-MM-DD)
- `analysisDate`: When the analysis was completed (YYYY-MM-DD)
- `dataSource`: Data provider (e.g., "FlipsideAI", "Dune", etc.)

**Note**: SQL queries, data files, and documentation are discoverable via the GitHub repository link—they don't need to be listed in this metadata file.

## TRACE Website Integration

The TRACE website will:

1. **Scan repositories** for `trace-metadata.json` files
2. **Extract metadata** to build the landing page snapshot cards
3. **Link to HTML files** via GitHub's raw content URL (opens in new tab)
4. **Display metadata** (author, networks, date range) from the JSON
5. **Provide links** to the GitHub repository where queries, data, and documentation can be found

### Linking to HTML Files

HTML reports are accessed via GitHub's raw content URL, which opens in a new tab:

**Raw Content URL Format:**
```
https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{htmlFile}
```

**Example:**
- Repository: `https://github.com/username/trace-aerodrome-rise`
- Branch: `main`
- HTML File: `aerodrome-rise.html`
- Raw URL: `https://raw.githubusercontent.com/username/trace-aerodrome-rise/main/aerodrome-rise.html`

**Implementation:**
```html
<a href="https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{htmlFile}" target="_blank" rel="noopener noreferrer">
  View Report
</a>
```

The HTML file should include a link back to the GitHub repository for users who want to explore queries, data, and documentation.

### HTML File Requirements

- Must be self-contained or use relative paths
- Should reference `styles.css` from the TRACE website (or include styles inline)
- Highcharts should use CDN or be self-hosted
- All data should be embedded in the HTML or use relative paths
- Should include a link to the GitHub repository (from `trace-metadata.json`) so users can access queries, data, and documentation

## Best Practices

1. **Keep it simple**: Static HTML, no build process required
2. **Self-contained**: Analysis should work when cloned standalone
3. **Document everything**: Include README with methodology, data sources, assumptions
4. **Version your data**: Commit data files to git (or use git LFS for large files)
5. **Tag releases**: Use git tags for major analysis versions
6. **Validate JSON**: Ensure `trace-metadata.json` is valid JSON before committing

## Example Workflow

```bash
# 1. Clone template
git clone <template-repo> my-new-analysis
cd my-new-analysis

# 2. Customize
mv content-template.html my-analysis.html
# Edit HTML, add queries, add data

# 3. Create metadata
cp trace-metadata.json.example trace-metadata.json
# Edit trace-metadata.json with your details

# 4. Commit and push
git add .
git commit -m "Initial analysis"
git remote add origin <your-repo-url>
git push -u origin main
```

## Example Repository

For a complete working example, see:

**[eth_fusaka](https://github.com/fsc-data-science/eth_fusaka)** — Median Ethereum Transaction Fees analysis with key upgrade milestones (2020–present)

This example demonstrates:
- Proper README structure for an analysis repo
- `trace-metadata.json` configuration
- Query → Data → Visual file relationships
- Final REPORT.html with embedded Highcharts visualization

## Questions?

See the main [TRACE website repository](https://github.com/fsc-data-science/TRACE) for integration details and website structure.
