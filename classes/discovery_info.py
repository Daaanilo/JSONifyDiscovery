from classes.dataset.dataset import Dataset
from classes.algorithm.algorithm import Algorithm
from classes.execution_info.execution_info import ExecutionInfo
from classes.execution.execution import Execution


class DiscoveryInfo:
    dataset: Dataset
    algorithm: Algorithm
    execution_info: ExecutionInfo
    execution: Execution
    extra: dict

    def __init__(self, dataset: Dataset, algorithm: Algorithm, execution_info: ExecutionInfo, execution: Execution, extra: str):
        self.dataset = dataset
        self.algorithm = algorithm
        self.execution_info = execution_info
        self.execution = execution
        self.extra = extra
        