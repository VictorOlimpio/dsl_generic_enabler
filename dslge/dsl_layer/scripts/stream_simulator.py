from dsl_layer.utils.load_tables import load_df_from_table
from dsl_layer.services.builders.measure_builder import MeasureBuilder
from dsl_layer.models import Measure
from random import seed
from random import random
import time

def run():
    Measure.objects.all().delete()
    df = load_df_from_table('medidas')
    measures = Measure.objects.all()
    seed(1)
    for index, row in df.iterrows():
        measure_builder = MeasureBuilder(row)
        measure_builder.save()
        if not measure_builder.errors is None:
            print('Error')
            break
        random_time = random()
        print('Instance inserted in: ' + str(random_time))
        time.sleep(random_time)
