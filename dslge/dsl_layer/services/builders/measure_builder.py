from dsl_layer.models import Measure


class MeasureBuilder:
    def __init__(self, measure_data):
        self.measure_data = measure_data
        self.errors = None

    def save(self):
        try:
            measure = self._build_instance(self.measure_data)
            measure.save()
            return measure
        except Exception as error:
            self.errors = str(error)

    def _build_instance(self, response):
        measure_one = response['medidaUm']
        measure_two = response['medidaDois']
        measure_three = response['medidaTres']
        measure_four = response['medidaQuatro']
        predicted_value = response['target']
        weekday = response['diaDeSemana']
        weekend = response['fimDeSemana']
        season = response['estacaoDoAno']
        return Measure(measure_one=measure_one,
                       measure_two=measure_two,
                       measure_three=measure_three,
                       measure_four=measure_four,
                       predicted_value=predicted_value,
                       weekday=weekday,
                       weekend=weekend,
                       season=season)
