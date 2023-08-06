import logging
import time

from nni.tuner import Tuner
from optimus import Optimus
from optimus.schemas import Metric, Parameter
from typing import Dict, List

logger = logging.getLogger('OptimusTuner')

class OptimusTuner(Tuner):
    """
    OptimusTuner is a tuner which integrating Optimus Optimization Engine.
    """

    def __init__(self, token: str= None, experiment: Dict = {}, metrics: List[Dict] = [], base_url: str = None, parallel_count: int = 1):
        """
        Parameters
        ----------
        token : str
            required, specify optimus API Token.
        experiment : dict
            "id", if set using existing experiment id, otherwise auto create new experiment each run.
            "name", optional for auto create experiment if no experiment id specified, should be as same as experimentName
            "paralle_count",  default is 1, but you should set a value same as NNI trialConcurrency
        metrics : List[Dict]
            optional, if experiment.id is set, metrics is ignored
            experiment metric, including:
                "name" str metric name
                "objective" str including "max", "min"
                "target" float objective target value, eg 0.99 mean 99% accuracy
                "range" [float, float] observed objective value range to narrow down search
            more details refers to https://aiexcelsior.art/docs/object/metric
        """

        self.experimentConfig = experiment

        self.metrics = [Metric(name=metric["name"],
                        objective=metric["objective"],
                        strategy="optimize",
                        target=metric["target"],
                        range=metric["range"]) for metric in metrics]

        self.optimus = Optimus(token=token, base_url=base_url)

    def receive_trial_result(self, parameter_id, parameters, value, **kwargs):
        """
        Record an observation of the objective function
        Parameters
        ----------
        parameter_id : int
            ignored for now
        parameters : dict
            ignored for now
        value : dict/float
            if value is dict, it should have "default" key, and other name must match name defined in metric
            value is final metrics of the trial, and will use the defined metric.name
        """
        value.pop('default')
        self.optimus.experiments(id=self.experiment_id).trials(id=self.trial.id).evaluate(evaluations=value)

    def generate_parameters(self, parameter_id, **kwargs):
        """
        Returns a set of trial (hyper-)parameters, as a serializable object.
        Parameters
        ----------
        parameter_id : int
        Returns
        -------
        params : dict
        """
        self.trial = self.optimus.experiments(id=self.experiment_id).start_one()
        return self.trial.assignment

    def update_search_space(self, search_space: Dict):
        """
        Create search space in Optimus when first setup experiment in case experiment_id not configured.
        Update search space not supported, will ignore subsequent calls.
        Parameters
        ----------
        search_space : dict
        """
        if self._safe_get(self.experimentConfig, "id") is not None:
            self.experiment_id = self._safe_get(self.experimentConfig, "id")
            logger.info("use existing experiment %s", self.experiment_id)
            return

        logger.info("creating new experiment with metric %s", self.metrics)

        parameters = []
        for x in search_space:
            if search_space[x]["_type"] == "choice":
                parameters.append(Parameter(name=x, type="c", range=[str(i) for i in search_space[x]['_value']]))
            elif search_space[x]["_type"] == "uniform":
                parameters.append(Parameter(name=x, type="r", range=search_space[x]['_value'], scale="linear", precision=5))
            elif search_space[x]["_type"] == "randint":
                parameters.append(Parameter(name=x, type="i", range=search_space[x]['_value']))
            elif search_space[x]["_type"] == "quniform":
                parameters.append(Parameter(name=x, type="i", range=search_space[x]['_value'][:2], step=search_space[x]['_value'][-1]))
            elif search_space[x]["_type"] == "loguniform":
                parameters.append(Parameter(name=x, type="r", range=search_space[x]['_value'], scale="log", precision=5))
            else:
                logger.warn("unsupported search_space name: %s, setting: %s, will be ignored.", x, search_space[x])

        name = self._safe_get(self.experimentConfig, "name", f"NNI_OptimusTuner_{int(time.time())}")
        parallel_count = self._safe_get(self.experimentConfig, "parallel_count", 1)

        self.experiment = self.optimus.create(name=name, description="", parallel_count=parallel_count, metrics=self.metrics, parameters=parameters)
        self.experiment_id = self.experiment.id
        self.optimus.experiments(self.experiment_id).start()

        logger.info("experiment %s created and started", self.experiment_id)


    def _safe_get(self, d: Dict, key: str, defaultValue = None):
        if key in d:
            return d[key]
        else:
            return defaultValue

