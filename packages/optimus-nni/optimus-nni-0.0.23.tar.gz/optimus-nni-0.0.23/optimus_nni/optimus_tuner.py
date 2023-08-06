from nni.tuner import Tuner
from optimus import Optimus
from typing import Dict


class OptimusTuner(Tuner):
    def __init__(self, token, experiment_id, metric_name, base_url: str = None):

        self.experiment_id = experiment_id
        self.metric_name = metric_name
        # 创建optimus对象
        self.optimus = Optimus(token=token, base_url=base_url)

    def receive_trial_result(self, parameter_id, parameters, value, **kwargs):

        # 将目标函数返回的结果value上传服务器端
        value.pop('default')
        self.optimus.experiments(id=self.experiment_id).trials(id=self.trial.id).evaluate(evaluations=value)

    def generate_parameters(self, parameter_id, **kwargs):

        # 从服务器端开始一次尝试并返回一组参数
        self.trial = self.optimus.experiments(id=self.experiment_id).start_one()
        return self.trial.assignment

    def update_search_space(self, search_space: Dict):
        '''
        Tuner 支持在运行时更新搜索空间。
        如果 Tuner 只在生成第一个超参前设置搜索空间，
        需要将其行为写到文档里。
        search_space: 定义 Experiment 时创建的 JSON 对象
        暂时不支持该功能，需要前往控制台手动创建实验
        '''

        
