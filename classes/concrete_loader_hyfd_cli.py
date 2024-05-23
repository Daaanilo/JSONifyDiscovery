from classes.abstract_loader import AbstractLoader
from classes.execution.execution import Execution
from classes.dataset.dataset import Dataset

import re
import json

class ConcreteLoader(AbstractLoader):

    def loadExecution(self, resultFile: str, dataset: Dataset) -> (Execution, str):
        execution = Execution(
            type=None,
            scenario=None,
            result={
                "data": []
            }
        )

        header = dataset.header

        with open(resultFile, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('{') and line.endswith('}'):
                    data = json.loads(line)
                    lhs = [{"column": header[int(item["columnIdentifier"].replace('column', '')) - 1], "comparison_relaxation": 0.0} for item in data["determinant"]["columnIdentifiers"]]

                    if "columnIdentifiers" in data["dependant"]:
                        rhs = [{"column": header[int(item["columnIdentifier"].replace('column', '')) - 1], "comparison_relaxation": 0.0} for item in data["dependant"]["columnIdentifiers"]]
                    else:
                        rhs = [{"column": header[int(data["dependant"]["columnIdentifier"].replace('column', '')) - 1], "comparison_relaxation": 0.0}]
                    
                    execution.result["data"].append({"lhs": lhs, "rhs": rhs})
                else:
                    match = re.match(r'([^->]+)\s*->\s*(.*)', line)
                    if match:
                        lhs = match.group(1).split('\t')
                        rhs = match.group(2).split('@')
                        data = {"lhs": [], "rhs": []}

                        for item in lhs:
                            if '@' in item:
                                column, value = item.split('@')
                                column_idx = int(column.replace('column', '').strip()) - 1
                                data["lhs"].append({"column": header[column_idx], "comparison_relaxation": float(value)})

                        if len(rhs) == 2:
                            column = rhs[0].strip()
                            column_idx = int(column.replace('column', '').strip()) - 1
                            value = rhs[1]
                            data["rhs"].append({"column": header[column_idx], "comparison_relaxation": float(value)})

                        execution.result["data"].append(data)

        return execution, "Attributi extra"
