from dsl_layer.models import Measures
from skmultiflow.data import DataStream, FileStream
from skmultiflow.data import WaveformGenerator
from skmultiflow.trees import HoeffdingTreeRegressor, HoeffdingTreeClassifier, HoeffdingTree
from skmultiflow.evaluation import EvaluatePrequential
from dsl_layer.utils.constants import DOC_DIR
from dsl_layer.utils.load_tables import load_df_from_table
import pandas as pd


def run():
    df = load_df_from_table('medidas')
    # df.rename(columns={'valor_predito': 'class'}, inplace=True)
    df_data = df[['medidaUm', 'medidaDois', 'medidaTres',
                  'medidaQuatro', 'diaDeSemana', 'fimDeSemana', 'estacaoDoAno']]
    df_target = df[['target']]
    # 1. Create a stream
    stream = DataStream(data=df_data, y=df_target)
    # 2. Instantiate the HoeffdingTreeClassifier
    ht = HoeffdingTreeRegressor()
    # 3. Setup the evaluator
    evaluator = EvaluatePrequential(show_plot=True,
                                    pretrain_size=200,
                                    max_samples=20000,
                                    metrics=['mean_square_error', 'mean_absolute_error'],
                                    output_file=DOC_DIR + 'results.csv')
    # 4. Run evaluation
    evaluator.evaluate(stream=stream, model=ht, model_names=['regression'])
