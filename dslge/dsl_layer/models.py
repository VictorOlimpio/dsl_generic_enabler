from django.db import models

# Create your models here.
class Measures(models.Model):
    measure_one = models.FloatField(null = True, db_column = 'measure_one')
    measure_two = models.FloatField(null = True, db_column = 'measure_two')
    measure_three = models.FloatField(null = True, db_column = 'measure_three')
    measure_four = models.FloatField(null = True, db_column = 'measure_four')
    predicted_value = models.FloatField(null = True, db_column = 'predicted_value')
    week_day = models.FloatField(null = True, db_column = 'week_day')
    weekend = models.FloatField(null = True, db_column = 'weekend')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'measures'