from classes.execution_info.system.system import System

class ExecutionInfo:
    system: System
    execution_command: str
    max_execution_time: str
    max_ram_usage: str
    start_time: str
    end_time: str

    def __init__(self, system: System, execution_command: str, max_execution_time: str, max_ram_usage: str,
                 start_time: str, end_time: str):
        self.system = system
        self.execution_command = execution_command
        self.max_execution_time = max_execution_time
        self.max_ram_usage = max_ram_usage
        self.start_time = start_time
        self.end_time = end_time