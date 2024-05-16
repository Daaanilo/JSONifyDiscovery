from classes.abstract_loader import AbstractLoader
from classes.dataset.dataset import Dataset
from classes.algorithm.algorithm import Algorithm
from classes.execution_info.execution_info import ExecutionInfo
from classes.execution.execution import Execution

import re

class ConcreteLoader(AbstractLoader):

    def loadExecution(self, resultFile: dict) -> (Execution, str):
        output = []

        with open(resultFile, 'r') as file:
            headers = None
            for line in file:
                line = line.strip()
                if line.startswith("Header:"):
                    headers = line.split(":")[1].strip().split(",")
                    break

        if headers is None:
            return None, "Failed to find headers."

        with open(resultFile, 'r') as file:
            for line in file:
                line = line.strip()
                match = re.match(r'"\((\d+(?:,\s*\d+)*)\) -> \((\d+(?:,\s*\d+)*)\)(?:\s+(?:KEY)?)?"', line)

                if match:
                    lhs_str = match.group(1)
                    rhs_str = match.group(2)

                    lhs_columns = [{"column": headers[int(x)], "comparison_relaxation": 0.0} for x in lhs_str.split(',')]
                    rhs_columns_indices = [int(x) for x in rhs_str.split(',')]
                    rhs_columns = [{"column": headers[index], "comparison_relaxation": 0.0} for index in rhs_columns_indices]

                    data = {"data": [{"lhs": lhs_columns, "rhs": rhs_columns}]}
                    output.append(data)

        return {"result": output}, "Attributi extra"
