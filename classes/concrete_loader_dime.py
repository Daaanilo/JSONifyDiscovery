from classes.abstract_loader import AbstractLoader
from classes.execution.execution import Execution

import re
import json

class ConcreteLoader(AbstractLoader):

    def loadExecution(self, resultFile: dict) -> (Execution, str):
        execution = Execution(
            type=None,
            scenario=None
        )
        execution_result = []

        with open(resultFile, 'r') as file:
            for line in file:
                line = line.strip()
                match = re.match(r'([^->]+)\s*->\s*(.*)', line)
                if match:
                    lhs = match.group(1).split('\t')
                    rhs = match.group(2).split('@')
                    data = {"lhs": [], "rhs": []}

                    for item in lhs:
                        if '@' in item:
                            column, value = item.split('@')
                            data["lhs"].append({"column": column.strip(), "comparison_relaxation": float(value)})

                    if len(rhs) == 2:
                        column = rhs[0].strip()
                        value = rhs[1]
                        data["rhs"].append({"column": column, "comparison_relaxation": float(value)})

                    execution_result.append({"data": [data]})

        execution.result = execution_result
        return execution, "Attributi extra"


