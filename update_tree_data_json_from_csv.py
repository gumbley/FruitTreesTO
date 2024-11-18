# Script to convert a CSV file of trees into a JSON file containing only fruit trees.
# Usage:
# 1. Modify the `input_csv` variable to point to your CSV file path.
# 2. Run the script in a terminal or command prompt using: python update_tree_data_json_from_csv.py
# 3. The output JSON file will be saved to the location specified by `output_json`.

import csv
import json

# Define a mapping of tree names to their fruiting schedules (start and end days of the year)
FRUIT_TREE_LIST = {
    'Apple': (244, 320),
    'Apple, common': (244, 320),
    'Apricot': (182, 212),
    'Cherry': (152, 181),
    'Cherry, black': (152, 181),
    'Cherry, sweet': (152, 181),
    'Mulberry': (182, 212),
    'Mulberry, red': (182, 212),
    'Mulberry, white': (182, 212),
    'Mulberry, white weeping': (182, 212),
    'Peach': (213, 243),
    'Pear': (213, 273),
    'Plum': (213, 243),
    'Plum, Canada': (213, 243),
    'Serviceberry': (152, 181),
    'Serviceberry Robin hill': (152, 181),
    'Serviceberry, smooth': (152, 181),
}

def process_csv_to_json(csv_file_path, json_file_path):
    # Read the CSV file and filter for fruit trees
    trees = []
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tree_name = row.get('COMMON_NAME', '').strip()
            if tree_name not in FRUIT_TREE_LIST:
                continue  # Skip non-fruit trees
            
            fruiting_start, fruiting_end = FRUIT_TREE_LIST[tree_name]

            # Split COMMON_NAME into name and sub_name
            name_parts = tree_name.split(',', 1)
            name = name_parts[0].strip()  # Everything before the comma
            sub_name = name_parts[1].strip() if len(name_parts) > 1 else ""  # Everything after the comma

            # Parse geometry as JSON and extract coordinates
            geometry = json.loads(row['geometry'])
            longitude, latitude = geometry['coordinates'][0]

            # Construct the address
            address = ' '.join([row['ADDRESS'].strip(), row['STREETNAME'].strip()])

            tree = {
                "city_id": row.get("STRUCTID", "").strip(),
                "name": name,
                "sub_name": sub_name,
                "latitude": latitude,
                "longitude": longitude,
                "address": address,
                "fruiting_start_day": fruiting_start,
                "fruiting_end_day": fruiting_end,
            }
            trees.append(tree)

    # Write the data to a JSON file
    with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(trees, jsonfile, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    # Example usage
    input_csv = r"C:\Users\...\StreetTreeData2024_11_15.csv"  # Replace with the actual CSV file path
    output_json = "tree_data.json"  # Replace with the desired JSON file path
    process_csv_to_json(input_csv, output_json)
