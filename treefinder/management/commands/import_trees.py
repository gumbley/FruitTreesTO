from django.core.management.base import BaseCommand
from treefinder.models import Tree
import csv
import json

class Command(BaseCommand):
    help = 'Import trees from a CSV file'

    # Define a list of common names for fruit trees and fruiting schedules
    fruit_tree_list = {
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

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to import.')


    def handle_row(self, row):
        try:
            geometry_str = row['geometry']
            coordinates_str = geometry_str.replace("{u'type': u'Point', u'coordinates': (", "").replace(")}", "")
            longitude, latitude = [float(coord) for coord in coordinates_str.split(', ')]

            # Use json.dumps to escape the string properly
            common_name = json.dumps(row['COMMON_NAME']).strip('"')
            address = ' '.join([row['ADDRESS'], row['STREETNAME']]).strip()
            address = json.dumps(address).strip('"')

            # Check for exact match in fruit tree list and get fruiting schedule
            if common_name in self.fruit_tree_list:
                fruiting_start_day, fruiting_end_day = self.fruit_tree_list[common_name]

                tree = Tree(
                    city_id=row['STRUCTID'],
                    name=common_name,
                    latitude=latitude,
                    longitude=longitude,
                    address=address,
                    fruiting_start_day=fruiting_start_day,
                    fruiting_end_day=fruiting_end_day
                )
                tree.save()
                
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f"Value error in row {row}: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error in row {row}: {e}"))

    def handle(self, *args, **options):
        with open(options['csv_file'], newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.handle_row(row)
