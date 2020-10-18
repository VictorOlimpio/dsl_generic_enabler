from dsl_core.models import Measure


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
        measure_one = response['medida_um']
        measure_two = response['medida_dois']
        measure_three = response['medida_tres']
        measure_four = response['medida_quatro']
        predicted_value = response['valor_predito']
        weekday = response['dia_de_semana']
        weekend = response['fim_de_semana']
        season = response['estacao_do_ano']
        return Measure(measure_one=measure_one,
                       measure_two=measure_two,
                       measure_three=measure_three,
                       measure_four=measure_four,
                       predicted_value=predicted_value,
                       weekday=weekday,
                       weekend=weekend,
                       season=season)
