
from dsl_layer.utils.constants import DOC_DIR
from dsl_layer.models import Measure
from dsl_layer.stream_learning_models.ml_processor import MLProcessor
from skmultiflow.trees import HoeffdingTreeRegressor
from django_pandas.io import read_frame


def run():
    df = read_frame(Measure.objects.all())
    # df.rename(columns={'valor_predito': 'class'}, inplace=True)
    df_data = df[['measure_one', 'measure_two', 'measure_three',
                  'measure_four', 'week_day', 'weekend', 'estacaoDoAno']]
    df_target = df[['predicted_value']]
    ht = HoeffdingTreeRegressor()
    stream_learning = MLProcessor(model=ht, metrics=['mean_square_error', 'mean_absolute_error'], params={
                                  'show_plot': True, 'pretrain_size': 200, 'max_samples': 60000, 
                                  'output_file': 'results.csv'})
    stream_learning.process(data=df_data, target=df_target)
