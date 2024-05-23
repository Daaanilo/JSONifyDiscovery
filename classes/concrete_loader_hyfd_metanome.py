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

        columns = []
        with open(resultFile, 'r') as file:
            found_column = False
            for line in file:
                line = line.strip()
                if line.startswith("# COLUMN"):
                    found_column = True
                elif found_column and line.startswith("1."):
                    column_data = line.split("\t")
                    column_name = column_data[0][2:]
                    columns.append((column_name, int(column_data[1])))

        columns.sort(key=lambda x: x[1])
        headers = [column[0] for column in columns]

        with open(resultFile, 'r') as file:
            for line in file:
                line = line.strip()
                match = re.match(r'(\d+(?:,\s*\d+)*)->(\d+(?:,\s*\d+)*)', line)

                if match:
                    lhs_str = match.group(1)
                    rhs_str = match.group(2)

                    lhs_columns = [{"column": headers[int(x) - 1], "comparison_relaxation": 0.0} for x in lhs_str.split(',')]
                    rhs_columns = [{"column": headers[int(x) - 1], "comparison_relaxation": 0.0} for x in rhs_str.split(',')]

                    data = {"lhs": lhs_columns, "rhs": rhs_columns}
                    execution.result["data"].append(data)

        return execution, "Attributi extra"
