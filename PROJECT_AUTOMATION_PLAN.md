# FruitTreesTO - Automation Plan

## Project Overview

**FruitTreesTO** is a GitHub Pages website that helps people find fruit trees in Toronto using an interactive map. The tree data comes from the City of Toronto's Street Tree Data, which is updated periodically.

- **Website URL**: Hosted on `gh-pages` branch
- **Data Source**: [City of Toronto Street Tree Data](https://open.toronto.ca/dataset/street-tree-data/)
- **Last Manual Update**: October 15, 2024 (noted in index.html:469)

## Current Architecture

### Key Files

1. **index.html** - Main website with interactive Leaflet map
   - Displays fruit trees with color-coded markers
   - Includes filtering by tree type and fruiting season
   - Shows "Last update: October 15, 2024" text on line 469
   - Loads tree data from `tree_data.json`

2. **tree_data.json** - Processed fruit tree data
   - Contains filtered tree records with lat/lng coordinates
   - Includes fruiting season metadata
   - Structure: `[{city_id, name, sub_name, latitude, longitude, address, fruiting_start_day, fruiting_end_day}]`

### Existing Python Scripts

#### 1. `update_automated.py` (87 lines)
**Purpose**: Full automation script that checks for updates and processes data

**Current Workflow**:
1. Fetches package metadata from Toronto Open Data API
2. Compares last modified date with stored `last_update.txt`
3. If updated:
   - Downloads new CSV file to `data/street_tree_data.csv`
   - Calls `update_tree_data_json_from_csv.py` to process CSV → JSON
   - Updates `last_update.txt` with new date
   - Commits and pushes changes to `gh-pages` branch

**Key Details**:
- Uses CKAN API: `https://ckan0.cf.opendata.inter.prod-toronto.ca`
- Package ID: `street-tree-data`
- Stores CSV in `data/` directory
- Git commands included (lines 80-82)
- **Does NOT update index.html date text**

#### 2. `update_tree_data_json_from_csv.py` (76 lines)
**Purpose**: Converts CSV street tree data to filtered JSON of fruit trees only

**Functionality**:
- Defines fruit tree list with fruiting schedules (lines 11-29)
- Filters CSV for only fruit-bearing trees
- Parses geometry JSON to extract coordinates
- Outputs formatted `tree_data.json`
- **Currently has hardcoded input path** (line 73) - needs to accept command-line argument

**Fruit Trees Tracked**:
- Apple (Aug 31 - Nov 16)
- Apricot (Jul 1 - Jul 31)
- Cherry (Jun 1 - Jun 30)
- Mulberry (Jul 1 - Jul 31)
- Peach (Aug 1 - Aug 31)
- Pear (Aug 1 - Sep 30)
- Plum (Aug 1 - Aug 31)
- Serviceberry (Jun 1 - Jun 30)

## Issues Identified

### 1. CLI Argument Issue
`update_tree_data_json_from_csv.py` is called with CLI arguments (line 74 of `update_automated.py`):
```python
subprocess.run(["python", "update_tree_data_json_from_csv.py", CSV_SAVE_PATH, json_output_path])
```

But the script doesn't accept CLI arguments - it uses hardcoded paths in `__main__`.

### 2. Missing Date Update in HTML
The automation script doesn't update the "Last update: October 15, 2024" text in `index.html` (line 469).

### 3. No GitHub Actions
Currently no `.github/workflows/` directory exists - all automation must be run manually.

## Automation Requirements

### Goal
Create a GitHub Action that runs monthly to:
1. Check City of Toronto API for data updates
2. Download and process new tree data if available
3. Update `tree_data.json`
4. Update the "Last update" date in `index.html` to current date when data changes
5. Commit and push changes automatically

### Questions for User

1. **Update Date Format**: When tree data updates, should the date in index.html be:
   - The current date (when the automation runs)?
   - The dataset's `metadata_modified` date from the API?
   - Current format uses: "October 15, 2024" - should we maintain this format?

2. **Schedule**: Monthly check is specified - preferred timing?
   - First day of month?
   - Mid-month?
   - Specific date?

3. **Notifications**: Should you be notified when:
   - Data is updated?
   - Check runs but no update found?
   - Process fails?

4. **Branch**: Currently targeting `gh-pages` - confirm this is correct?

5. **Commit Messages**: Preferred format? Current script uses:
   - "Updated tree data (YYYY-MM-DDTHH:MM:SS)"

## Recommended Implementation Plan

### Phase 1: Fix Existing Scripts
1. **Fix `update_tree_data_json_from_csv.py`** to properly accept CLI arguments
2. **Add HTML date update** functionality to `update_automated.py`
3. **Test locally** to ensure the full pipeline works

### Phase 2: Create GitHub Action
1. Create `.github/workflows/` directory structure
2. Create workflow YAML file for monthly scheduled runs
3. Configure Python environment with dependencies
4. Set up git credentials for automated commits
5. Add error handling and notifications

### Phase 3: Testing & Documentation
1. Test workflow manually via GitHub Actions UI
2. Document the automation process
3. Update README.md with automation details

## Technical Considerations

### GitHub Actions Requirements
- Python 3.x environment
- Dependencies: `requests`, `beautifulsoup4` (if needed)
- Git configuration for automated commits
- Proper permissions for pushing to `gh-pages`
- Schedule using cron syntax (monthly)

### Script Modifications Needed
1. Make `update_tree_data_json_from_csv.py` accept sys.argv properly
2. Add function to update date in index.html (regex or string replacement)
3. Add better error handling and logging
4. Consider adding a flag to force-update even if date hasn't changed

## Implementation Summary

### Completed Changes

#### 1. Fixed `update_tree_data_json_from_csv.py` (Lines 71-84)
- Added proper CLI argument handling using `sys.argv`
- Script now accepts: `python update_tree_data_json_from_csv.py <input_csv> <output_json>`
- Falls back to defaults if no arguments provided
- Compatible with `update_automated.py` subprocess call

#### 2. Enhanced `update_automated.py`
**New imports** (Lines 5-6):
- Added `re` for regex-based HTML updates
- Added `datetime` for date formatting

**New function** `update_html_date()` (Lines 58-81):
- Parses API's ISO date format (e.g., "2024-10-15T14:23:45")
- Converts to readable format (e.g., "October 15, 2024")
- Updates `index.html` line 469 using regex pattern matching
- Returns formatted date for commit message

**Updated workflow in `main()`**:
- Step 5: Calls `update_html_date()` to update index.html
- Step 7: Adds `index.html` to git commit
- New commit message format: "Update tree data - New dataset from {formatted_date}"

#### 3. Created GitHub Actions Workflow
**File**: `.github/workflows/update-tree-data.yml`

**Triggers**:
- Scheduled: 1st of every month at 2 AM UTC
- Manual: Via GitHub Actions UI (workflow_dispatch)

**Workflow steps**:
1. Checkout `gh-pages` branch
2. Set up Python 3.11
3. Install dependencies (requests)
4. Configure git with github-actions bot credentials
5. Run `update_automated.py`
6. Automatic commit & push handled by Python script
7. Success/failure notifications via GitHub Actions UI

**Permissions**:
- `contents: write` for pushing commits

### Files Modified
- `update_tree_data_json_from_csv.py` - CLI argument support
- `update_automated.py` - HTML date updates, improved commit messages
- `index.html` - Will be auto-updated by workflow

### Files Created
- `.github/workflows/update-tree-data.yml` - Monthly automation workflow

## How It Works

### Automated Monthly Flow
1. **Trigger**: GitHub Action runs on the 1st of each month
2. **Check**: Script fetches Toronto Open Data API metadata
3. **Compare**: Compares `metadata_modified` date with `last_update.txt`
4. **Update** (if new data available):
   - Downloads new CSV file
   - Processes to JSON (fruit trees only)
   - Updates index.html with new date
   - Commits changes with descriptive message
   - Pushes to `gh-pages` branch
5. **Skip** (if no update): Exits gracefully

### Manual Testing
You can trigger the workflow manually:
1. Go to GitHub repository → Actions tab
2. Select "Update Toronto Tree Data" workflow
3. Click "Run workflow" → Run on `gh-pages` branch

### Monitoring
- **Success**: Check Actions tab for green checkmark
- **Failure**: GitHub will send email notification (if enabled in settings)
- **Logs**: Available in Actions tab for debugging

## Next Steps for Deployment

1. **Commit these changes** to the `gh-pages` branch:
   ```bash
   git add .
   git commit -m "Add automated monthly tree data updates via GitHub Actions"
   git push origin gh-pages
   ```

2. **Enable GitHub Actions** (if not already enabled):
   - Go to repository Settings → Actions → General
   - Ensure "Allow all actions and reusable workflows" is selected

3. **Test the workflow manually**:
   - Go to Actions tab
   - Select "Update Toronto Tree Data"
   - Click "Run workflow"
   - Monitor the run to ensure it works

4. **Wait for first scheduled run** on the 1st of next month, or manually trigger to test immediately

## Troubleshooting

### Common Issues
- **Permission denied on push**: Check repository Settings → Actions → General → Workflow permissions → Enable "Read and write permissions"
- **Python import errors**: Ensure all dependencies are in `requirements.txt` or installed in workflow
- **API connection issues**: Toronto Open Data API may be temporarily unavailable
- **No changes detected**: Dataset may not have been updated since last check
