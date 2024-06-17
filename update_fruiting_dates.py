"""
Instructions to Run the Script:
1. Save the above script as update_fruiting_dates.py in your project directory.
2. Make sure tree_data.json is in the same directory as the script or provide the correct path.
3. Open Command Prompt and navigate to the directory where the script is saved.
4. Run the script using the following command:
   python update_fruiting_dates.py
5. This will update all the Mulberry trees' fruiting_start_day and fruiting_end_day in tree_data.json.
"""

import json

def update_fruiting_dates(file_path, tree_name, new_start_day, new_end_day):
    # Read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Update the fruiting dates for the specified tree name
    for tree in data:
        if tree['name'] == tree_name:
            tree['fruiting_start_day'] = new_start_day
            tree['fruiting_end_day'] = new_end_day

    # Write the updated data back to the JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Example usage
file_path = 'tree_data.json'
tree_name = 'Mulberry'
new_start_day = 165  # Replace with the desired start day
new_end_day = 212    # Replace with the desired end day

update_fruiting_dates(file_path, tree_name, new_start_day, new_end_day)
