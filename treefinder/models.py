from django.db import models
from django.core.exceptions import ValidationError

class Tree(models.Model):
    city_id = models.CharField(max_length=50, unique=True)  # Unique ID from City of Toronto data
    name = models.CharField(max_length=100)  # Broad category, e.g., 'Mulberry'
    sub_name = models.CharField(max_length=100, blank=True, null=True)  # Specific type, e.g., 'White'
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(blank=True, null=True)  # Optional
    fruiting_start_day = models.IntegerField()  # Day of year when fruiting starts
    fruiting_end_day = models.IntegerField()  # Day of year when fruiting ends
    address = models.CharField(max_length=255, blank=True, null=True)  # Optional

    def clean(self):
        # Validation to ensure start day is before end day
        if self.fruiting_start_day >= self.fruiting_end_day:
            raise ValidationError("Fruiting start day must be before fruiting end day.")

    def __str__(self):
        tree_type = f"{self.name} {' - ' + self.sub_name if self.sub_name else ''}"
        return f"{tree_type} tree at {self.address or 'coordinates: (%s, %s)' % (self.latitude, self.longitude)}"

    @property
    def fruiting_season(self):
        # Convert day numbers to more readable date format
        start_date = self.day_of_year_to_date(self.fruiting_start_day)
        end_date = self.day_of_year_to_date(self.fruiting_end_day)
        return f"{start_date} to {end_date}"

    @staticmethod
    def day_of_year_to_date(day_of_year):
        from datetime import datetime
        return datetime.strptime(f'{day_of_year} 2023', '%j %Y').strftime('%B %d')
