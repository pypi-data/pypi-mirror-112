from nni.tuner import Tuner
from optimus import Optimus
from optimus.schemas import Metric, Parameter
from typing import Dict


class OptimusTuner(Tuner):
    def __init__(self, token, experiment_id, metric: Dict):
        if experiment_id:
            self.experiment_id = experiment_id
        else:
            metric = Metric(name=metric["name"], objective=metric["mode"], strategy="optimize", target=metric["target"],
                            range=metric["range"])
            self.metric = [metric]
        # 创建optimus对象
        self.optimus = Optimus(token=token)

    def receive_trial_result(self, parameter_id, parameters, value, **kwargs):

        # 将目标函数返回的结果value上传服务器端
        value.pop('default')
        self.optimus.experiments(id=self.experiment_id).trials(id=self.trial.id).evaluate(evaluations=value)

    def generate_parameters(self, parameter_id, **kwargs):

        # 从服务器端开始一次尝试并返回一组参数
        self.trial = self.optimus.experiments(id=self.experiment_id).start_one()
        return self.trial.assignment

    def update_search_space(self, search_space: Dict):

        if hasattr(self, "experiment_id"):
            return
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
        experiment = self.optimus.create(name="nni_create", description="it is created by nni", parallel_count=5, metrics=self.metric, parameters=parameters)
        self.experiment_id = experiment.id
        self.optimus.experiments(self.experiment_id).start()


