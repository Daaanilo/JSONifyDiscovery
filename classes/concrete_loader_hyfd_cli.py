from classes.abstract_loader import AbstractLoader
from classes.execution.execution import Execution

import json

class ConcreteLoader(AbstractLoader):

    def loadExecution(self, resultFile: str) -> (Execution, str):
        execution = Execution(
            type=None,
            scenario=None
        )
        output = {"result": []}

        with open(resultFile, 'r') as file:
            for line in file:
                line = line.strip()
                data = json.loads(line)
                lhs = [{"column": item["columnIdentifier"], "comparison_relaxation": 0.0} for item in data["determinant"]["columnIdentifiers"]]
                
                if "columnIdentifiers" in data["dependant"]:
                    rhs = [{"column": item["columnIdentifier"], "comparison_relaxation": 0.0} for item in data["dependant"]["columnIdentifiers"]]
                else:
                    rhs = [{"column": data["dependant"]["columnIdentifier"], "comparison_relaxation": 0.0}]
                
                output["result"].append({"data": [{"lhs": lhs, "rhs": rhs}]})

        return output, "Attributi extra"
