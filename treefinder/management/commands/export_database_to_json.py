import json
from treefinder.models import Tree

trees = Tree.objects.all()
tree_data = []

for tree in trees:
    tree_data.append({
        "city_id": tree.city_id,
        "name": tree.name,
        "latitude": tree.latitude,
        "longitude": tree.longitude,
        "address": tree.address,
        "fruiting_start_day": tree.fruiting_start_day,
        "fruiting_end_day": tree.fruiting_end_day
    })

with open('tree_data.json', 'w') as f:
    json.dump(tree_data, f)
