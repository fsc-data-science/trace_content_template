# Rebuild Instructions

This document describes how to rebuild the final REPORT.html from the component files (DATA, QUERY, VISUAL) without re-running SQL queries.

## Pre-Flight Checklist

Before building or modifying analyses, verify:

- [ ] **UV installed**: `uv run python --version` works
- [ ] **FlipsideAI MCP key configured** (for running queries)
- [ ] **Read `highcharts_embedding_guide.md`** for chart conventions

## Highcharts Best Practices

See `highcharts_embedding_guide.md` for complete documentation. Key rules:

1. **Use built-in `format:` strings** — avoid custom `formatter: function()` 
2. **Colors**: Use the high-contrast palette (`#0000B9`, `#FF2424`, etc.)
3. **Credits**: Set to `'Data: FlipsideAI'`
4. **No subtitles** unless specifically needed
5. **X-axis dates**: Use `{value:%b '%y}` format (e.g., "Jan '20")

## File Structure

```
analysis-repo/
├── REPORT.html              # Final standalone HTML report (to be generated)
├── content-template.html    # Template/base HTML file
├── queries/                 # SQL query files (01_*.sql, 02_*.sql, ...)
├── data/                    # JSON data files (01_*.json, 02_*.json, ...)
├── visuals/                  # Highcharts visualization files (VIZTYPE_TITLE.html)
├── utils/                    # Utility scripts
│   └── swap_placeholder.py  # Placeholder replacement utility
├── pyproject.toml           # UV project configuration
└── trace-metadata.json      # Metadata with file mappings
```


## File Relationships

- **QUERY → DATA**: 1:1 relationship
  - `queries/01_market_share.sql` → `data/01_market_share.json`
  - `queries/02_volume_analysis.sql` → `data/02_volume_analysis.json`

- **DATA → VISUAL**: 1:many relationship
  - `data/01_market_share.json` → `visuals/AREA_market_share_weekly.html`
  - `data/01_market_share.json` → `visuals/LINE_market_share_daily.html`
  - `data/02_volume_analysis.json` → `visuals/BAR_volume_by_pool.html`

## Assembly Process

### Step 1: Start with Template

Begin with `content-template.html` as the base structure.

### Step 2: Embed Data Files

Instead of manually pasting large JSON objects, use the `swap_placeholder.py` utility.

1. In your HTML file, create a variable with a unique placeholder:
   ```html
   <script>
     const data01 = {{DATA_01_PLACEHOLDER}};
   </script>
   ```

2. Run the swap utility to inject the JSON content:
   ```bash
   uv run python utils/swap_placeholder.py REPORT.html "{{DATA_01_PLACEHOLDER}}" data/01_market_share.json
   ```

### Step 3: Embed Query Text

Similarly, use placeholders for SQL queries to keep your HTML template clean.

1. In your HTML file:
   ```html
   <details class="query-section">
     <summary>View SQL Query</summary>
     <pre><code class="sql">{{QUERY_01_PLACEHOLDER}}</code></pre>
   </details>
   ```

2. Run the swap utility:
   ```bash
   uv run python utils/swap_placeholder.py REPORT.html "{{QUERY_01_PLACEHOLDER}}" queries/01_market_share.sql
   ```

### Step 4: Embed Visuals

For Visuals, you can also inject the entire chart container and script if they are self-contained in the `visuals/` folder, or just inject the Highcharts configuration object if you prefer.

**Option A: Inject Full Visual File (Recommended)**

1. In `visuals/AREA_market_share_weekly.html`, ensure you have the chart container and script.
2. In `REPORT.html`, place a placeholder where the chart should go:
   ```html
   <!-- Chart Section -->
   <div class="chart-wrapper">
     {{VISUAL_01_PLACEHOLDER}}
   </div>
   ```
3. Run the swap utility:
   ```bash
   uv run python utils/swap_placeholder.py REPORT.html "{{VISUAL_01_PLACEHOLDER}}" visuals/AREA_market_share_weekly.html
   ```

**Note on Visuals**: If your `visuals/` files contain full `<html>` tags, you might want to strip them before injecting, or ensure your `swap_placeholder.py` usage is targeted correctly. The `swap_placeholder.py` script does a literal replacement of the entire file content.

### Step 5: Update Metadata Sections

Update the following sections in the REPORT:
- Table of Contents (TOC) with all sections
- Author, Reviewer, Network(s), Timestamp Range, Data Source
- Any metadata from `trace-metadata.json`

### Step 6: Finalize

1. Ensure all CSS is either:
   - Inlined in `<style>` tags (to keep REPORT fully standalone)
2. Ensure Highcharts is loaded (CDN or local)
3. Test that the REPORT is fully standalone (no external dependencies)
4. Save as the final REPORT filename (e.g., `aerodrome-rise.html`)

## Example Mapping

Based on `trace-metadata.json`, create a mapping like:

```javascript
const fileMapping = {
  "01_market_share": {
    query: "queries/01_market_share.sql",
    data: "data/01_market_share.json",
    visuals: [
      "visuals/AREA_market_share_weekly.html",
      "visuals/LINE_market_share_daily.html"
    ]
  },
  "02_volume_analysis": {
    query: "queries/02_volume_analysis.sql",
    data: "data/02_volume_analysis.json",
    visuals: [
      "visuals/BAR_volume_by_pool.html"
    ]
  }
};
```

## Validation Checklist

Before finalizing the REPORT:

- [ ] All DATA files are embedded
- [ ] All QUERY files are embedded  
- [ ] All VISUAL files are embedded
- [ ] **VISUAL files match REPORT** (keep them in sync!)
- [ ] TOC is updated and links work
- [ ] Metadata sections are filled in
- [ ] REPORT is standalone (no broken external references)
- [ ] Highcharts loads and renders correctly
- [ ] All charts display with correct data
- [ ] Credits show "Data: FlipsideAI"
- [ ] Colors follow `highcharts_embedding_guide.md` palette
- [ ] No custom formatter functions (use `format:` strings)

