
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
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt


def run(*args):
    max_samples = np.int(args[0])
    Measure.objects.all().delete()
    # 1. Instantiate the HoeffdingTreeClassifier
    ht = HoeffdingTreeRegressor()

    evaluate(ht, max_samples)


def evaluate(model, max_samples):
    n_samples = 0
    # Buffering 93 samples to pre-train on 92 and get the next sample
    while(n_samples <= 93):
        df = read_frame(Measure.objects.all())
        n_samples = len(df)
    next_sample = df.tail(1)
    df = df[:92]
    df_data = df[['measure_one', 'measure_two', 'measure_three',
                  'measure_four', 'weekday', 'weekend', 'season']]
    df_target = df[['predicted_value']]
    stream = DataStream(data=df_data, y=df_target)
    # Pre-training
    pre_train_size = len(df)
    X, y = stream.next_sample(pre_train_size)
    model.partial_fit(X, y)
    # Preparing to evaluate
    y_pred, y_true = np.zeros(max_samples), np.zeros(max_samples)
    df = next_sample
    stream = prepare_stream(df)
    result = pd.DataFrame(
        columns=['total_samples', 'pre_trained_samples', 'MAE', 'MSE'])
    # Evaluate
    while(n_samples < max_samples and stream.has_more_samples()):
        X, y = stream.next_sample()
        y_true[n_samples] = y[0]
        y_pred[n_samples] = model.predict(X)[0]
        model.partial_fit(X, y)
        # Loading the next sample
        current_sample = Measure.objects.get(id=df.iloc[-1]['id'])
        next_sample = pd.DataFrame(columns=df.columns)
        while(next_sample.empty):
            try:
                next_sample = pd.DataFrame(
                    [model_to_dict(current_sample.get_next_by_created_at())])
            except Exception as error:
                continue
        # Preparing the next evaluation
        df = next_sample
        stream = prepare_stream(df)
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        result_summary(n_samples, pre_train_size, mae, mse)
        result_dict = {'total_samples': n_samples,
                       'pre_trained_samples': pre_train_size, 'MAE': mae, 'MSE': mse}
        result = result.append(result_dict, ignore_index=True)
        n_samples += 1
    result.plot(x ='total_samples', y='MAE', kind = 'line')
    result.plot(x ='total_samples', y='MSE', kind = 'line')
    plt.show()


def prepare_stream(sample):
    df_data = sample[['measure_one', 'measure_two', 'measure_three',
                      'measure_four', 'weekday', 'weekend', 'season']]
    df_target = sample[['predicted_value']]
    return DataStream(data=df_data, y=df_target)


def result_summary(n_samples, pre_train_size, mae, mse):
    print('{} samples analyzed.'.format(n_samples))
    print('Pre trained on {} samples.'.format(pre_train_size))
    print('Hoeffding Tree regressor MAE: {}'.
          format(mae))
    print('Hoeffding Tree regressor MSE: {}'.
          format(mse))

