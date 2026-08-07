import requests
import os
import json
import subprocess
import re
from datetime import datetime

# Constants
BASE_URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
PACKAGE_ID = "street-tree-data"
LAST_UPDATE_FILE = "last_update.txt"
CSV_SAVE_PATH = "data/street_tree_data.csv"
INDEX_HTML_PATH = "index.html"

# Ensure the data directory exists
os.makedirs("data", exist_ok=True)

def fetch_package_metadata():
    """Fetch metadata for the package."""
    url = f"{BASE_URL}/api/3/action/package_show"
    params = {"id": PACKAGE_ID}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_last_updated_date(metadata):
    """Retrieve the dataset's last updated date."""
    return metadata["result"]["metadata_modified"]

def get_csv_url(metadata):
    """Find the URL of the CSV file in the package resources."""
    for resource in metadata["result"]["resources"]:
        if resource["format"].lower() == "csv":
            return resource["url"]
    raise ValueError("CSV resource not found in the package.")

def get_previous_update_date():
    """Read the stored last update date."""
    if os.path.exists(LAST_UPDATE_FILE):
        with open(LAST_UPDATE_FILE, 'r') as f:
            return f.read().strip()
    return None

def save_update_date(date):
    """Save the new update date to the file."""
    with open(LAST_UPDATE_FILE, 'w') as f:
        f.write(date)

def download_csv(csv_url):
    """Download the CSV dataset."""
    print(f"Downloading dataset from {csv_url}...")
    response = requests.get(csv_url)
    response.raise_for_status()
    with open(CSV_SAVE_PATH, 'wb') as f:
        f.write(response.content)
    print(f"Dataset saved to {CSV_SAVE_PATH}.")

def update_html_date(date_string):
    """Update the 'Last update' date in index.html."""
    # Parse the ISO format date string (e.g., "2024-10-15T14:23:45")
    date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00').split('T')[0])

    # Format to readable format: "October 15, 2024"
    formatted_date = date_obj.strftime("%B %d, %Y")

    # Read the HTML file
    with open(INDEX_HTML_PATH, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Replace the last update date using regex
    # Pattern matches: <p>Last update: [any date format]</p>
    pattern = r'(<p>Last update: )([^<]+)(</p>)'
    replacement = rf'\g<1>{formatted_date}\g<3>'
    updated_html = re.sub(pattern, replacement, html_content)

    # Write back to the file
    with open(INDEX_HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(updated_html)

    print(f"Updated index.html with date: {formatted_date}")
    return formatted_date

def main():
    # Step 1: Fetch package metadata
    metadata = fetch_package_metadata()
    last_updated_date = get_last_updated_date(metadata)

    # Step 2: Compare dates to check for updates
    previous_date = get_previous_update_date()
    if previous_date == last_updated_date:
        print("The dataset has not been updated since the last check.")
        return
    else:
        print(f"New update found! Last modified: {last_updated_date}")

    # Step 3: Download the updated CSV file
    csv_url = get_csv_url(metadata)
    download_csv(csv_url)

    # Step 4: Process the CSV into JSON
    json_output_path = "tree_data.json"
    subprocess.run(["python", "update_tree_data_json_from_csv.py", CSV_SAVE_PATH, json_output_path])

    # Step 5: Update the date in index.html
    formatted_date = update_html_date(last_updated_date)

    # Step 6: Save the new update date
    save_update_date(last_updated_date)

    # Step 7: Commit and push changes to GitHub
    subprocess.run(["git", "add", "tree_data.json", "last_update.txt", "index.html"])
    commit_message = f"Update tree data - New dataset from {formatted_date}"
    subprocess.run(["git", "commit", "-m", commit_message])
    subprocess.run(["git", "push", "origin", "gh-pages"])
    print("Tree data updated and pushed to GitHub.")

if __name__ == "__main__":
    main()
