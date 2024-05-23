from classes.execution.result.result import Result

class Execution:
    type: str
    scenario: str
    result: list[Result]

    def __init__(self, type=str, scenario=str, result=list[Result]):
        self.type = type
        self.scenario = scenario
        self.result = result if result else []