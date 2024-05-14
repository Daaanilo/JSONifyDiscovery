from classes.execution.result.time_execution.time_execution import TimeExecution
from classes.execution.result.ram_usage.ram_usage import RamUsage
from classes.execution.result.error.error import Error
from classes.execution.result.additional_info.additional_info import AdditionalInfo
from classes.execution.result.data.data import Data

class Result:
    time_execution: TimeExecution
    ram_usage: RamUsage
    error: Error
    additional_info: AdditionalInfo
    data: list[Data]

    def __init__(self, time_execution: TimeExecution, ram_usage: RamUsage, error: Error, additional_info: AdditionalInfo,
                 data: list[Data]):
        self.time_execution = time_execution
        self.ram_usage = ram_usage
        self.error = error
        self.additional_info = additional_info
        self.data = data