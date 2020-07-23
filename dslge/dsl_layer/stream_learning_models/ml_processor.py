from dsl_layer.models import Measures
from skmultiflow.data import DataStream
from skmultiflow.evaluation import EvaluatePrequential
from dsl_layer.utils.constants import DOC_DIR


class MLProcessor:
    EVALUETE_PARAMS_KEYS = ['n_wait', 'max_samples', 'batch_size', 'pretrain_size', 'max_time',
                            'output_file', 'show_plot', 'restart_stream', 'data_points_for_classification']

    def __init__(self, model, metrics=['accuracy', 'kappa'], params={}):
        self.model = model
        self.metrics = metrics
        self.params = params
        self.errors = {}

    def process(self, data, target):
        # 1. Create a stream
        stream = DataStream(data=data, y=target)
        # 2. Setup the evaluator
        # Validating params
        if self._validate_evaluate_params:
            evaluator = EvaluatePrequential(max_samples=self.params['max_samples'],
                                            output_file=DOC_DIR +
                                            self.params['output_file'],
                                            show_plot=self.params['show_plot'],
                                            metrics=self.metrics)
        if not self.errors:
            # 3. Run evaluation
            evaluator.evaluate(stream=stream, model=self.model)

    def _validate_evaluate_params(self):
        if self.params is None or not self.params:
            self.errors = {'error:' 'Error: Evaluate param must not be empty'}
            return False
        if all(key in self.params for key in self.EVALUETE_PARAMS_KEYS):
            return True

    def _validate_model_params(self):
        if self.params is None or not self.params:
            self.errors = {'error:' 'Error: Model param must not be empty'}
            return False
        if all(key in self.params for key in self.EVALUETE_PARAMS_KEYS):
            return True
