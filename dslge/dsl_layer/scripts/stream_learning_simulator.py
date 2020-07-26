
from dsl_layer.utils.constants import DOC_DIR
from dsl_layer.models import Measure
from dsl_layer.stream_learning_models.ml_processor import MLProcessor
from skmultiflow.trees import HoeffdingTreeRegressor
from django_pandas.io import read_frame
from dsl_layer.utils.load_tables import load_df_from_table
from skmultiflow.evaluation import EvaluatePrequential
from skmultiflow.data import DataStream
import pandas as pd
from django.forms import model_to_dict
import numpy as np


def run(*args):
    n_samples = np.int(args[0])
    Measure.objects.all().delete()
    # 1. Instantiate the HoeffdingTreeClassifier
    ht = HoeffdingTreeRegressor()
    # 2. Setup the evaluator
    evaluator = EvaluatePrequential(show_plot=True,
                                    n_wait=1,
                                    pretrain_size=92,
                                    max_samples=50000,
                                    restart_stream=False,
                                    output_file=DOC_DIR + 'results.csv',
                                    metrics=['mean_square_error', 'mean_absolute_error'])
    count = 0
    # 3. Buffering 94 samples to pre-train on 92, evaluate on 1 and get the next sample
    # while(count <= 94):
    #     df = read_frame(Measure.objects.all())
    #     count = len(df)
    # next_sample = df.tail(1)
    # df = df[:93] 
    while(count <= n_samples):
        df = read_frame(Measure.objects.all())
        count = len(df)
    df_data = df[['measure_one', 'measure_two', 'measure_three',
                'measure_four', 'weekday', 'weekend', 'season']]
    df_target = df[['predicted_value']]
    stream = DataStream(data=df_data, y=df_target)
    evaluator.evaluate(stream, model=ht)
    # df = df.append(next_sample) # Append the next sample to be evaluated
    # 4. Run evaluation
    # while(not next_sample.empty):
    #     df = next_sample
    #     df_data = df[['measure_one', 'measure_two', 'measure_three',
    #                 'measure_four', 'weekday', 'weekend', 'season']]
    #     df_target = df[['predicted_value']]
    #     stream = DataStream(data=df_data, y=df_target)
    #     # import ipdb; ipdb.set_trace()
    #     # X = df_data.to_numpy()
    #     # evaluator.predict(X=X)
    #     # evaluator.partial_fit(X=X, y=df_target.to_numpy())
    #     # evaluator = evaluator.evaluation_summary()
    #     evaluator.evaluate(stream, model=ht)
    #     current_sample = Measure.objects.get(id=df.iloc[-1]['id'])
    #     next_sample = pd.DataFrame(columns=df.columns)
    #     # Loading the next sample
    #     while(next_sample.empty):
    #         try:
    #             next_sample = pd.DataFrame([model_to_dict(current_sample.get_next_by_created_at())])
    #         except Exception as error:
    #             continue
    #     # df = df.append(next_sample)
