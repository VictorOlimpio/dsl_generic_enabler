
from dsl_layer.utils.constants import DOC_DIR
from dsl_layer.utils.load_tables import load_df_from_table
from dsl_layer.stream_learning_models.ml_processor import MLProcessor
from skmultiflow.trees import HoeffdingTreeRegressor

def run():
    df = load_df_from_table('medidas')
    # df.rename(columns={'valor_predito': 'class'}, inplace=True)
    df_data = df[['medidaUm', 'medidaDois', 'medidaTres',
                  'medidaQuatro', 'diaDeSemana', 'fimDeSemana', 'estacaoDoAno']]
    df_target = df[['target']]
    ht = HoeffdingTreeRegressor()
    stream_learning = MLProcessor(model=ht, metrics=['mean_square_error', 'mean_absolute_error'], params={
                                  'show_plot': True, 'pretrain_size': 200, 'max_samples': 60000, 'output_file': 'results.csv'})
    stream_learning.process(data=df_data, target=df_target)