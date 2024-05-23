from classes.abstract_loader import AbstractLoader
from classes.execution.execution import Execution
from classes.dataset.dataset import Dataset

import re

class ConcreteLoader(AbstractLoader):

    def loadExecution(self, resultFile: str, dataset: Dataset) -> (Execution, str):
        execution = Execution(
            type=None,
            scenario=None,
            result={
                "data": []
            }
        )

        headers = dataset.header

        if headers is None:
            return None, "Header non trovato."

        with open(resultFile, 'r') as file:
            for line in file:
                line = line.strip()
                match = re.match(r'"\((\d+(?:,\s*\d+)*)\) -> \((\d+(?:,\s*\d+)*)\)(?:\s+(?:KEY)?)?"', line)

                if match:
                    lhs_str = match.group(1)
                    rhs_str = match.group(2)

                    lhs_columns = [{"column": headers[int(x)], "comparison_relaxation": 0.0} for x in lhs_str.split(',')]

                    for index in rhs_str.split(','):
                        rhs_columns = [{"column": headers[int(index)], "comparison_relaxation": 0.0}]
                        data = {"lhs": lhs_columns, "rhs": rhs_columns}
                        execution.result["data"].append(data)

        return execution, "Attributi extra"
