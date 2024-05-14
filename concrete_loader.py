from classes.abstract_loader import AbstractLoader
from classes.dataset.dataset import Dataset
from classes.algorithm.algorithm import Algorithm
from classes.execution_info.execution_info import ExecutionInfo
from classes.execution.execution import Execution

import re
import json

class ConcreteLoader(AbstractLoader):
    def loadExecution(self, resultFile: dict) -> (Execution, str):
        execution = Execution(
            type=None,
            scenario=None
        )

        try:
            with open(resultFile, "r") as f:
                log_content = f.read()

                execution.result = []
                dependency_matches = re.findall(r"(\w+)\@([\d.]+)\s+(?:->)\s+(\w+)\@([\d.]+)", log_content)
                if dependency_matches:
                    lhs_columns = []
                    lhs_relaxations = []
                    rhs_columns = []
                    rhs_relaxations = []

                    for match in dependency_matches:
                        lhs_columns.append(match[0])
                        lhs_relaxations.append(float(match[1]))
                        rhs_columns.append(match[2])
                        rhs_relaxations.append(float(match[3]))

                    if not execution.result:
                        execution.result = []
                    execution.result.append({
                        "dependencies": {
                            "lhs": {
                                "column": lhs_columns,
                                "comparison_relaxation": lhs_relaxations
                            },
                            "rhs": {
                                "column": rhs_columns,
                                "comparison_relaxation": rhs_relaxations
                            }
                        }
                    })


                memory_match = re.search(r"Memory consumption:\s+(\d+)\s*([a-zA-Z]+)", log_content, re.MULTILINE)
                if memory_match:
                    max_ram_used = memory_match.group(1)
                    unit = memory_match.group(2)
                    if not execution.result:
                        execution.result = []
                    execution.result.append({
                        "ram_usage": {
                            "max_ram_used": max_ram_used,
                            "unit": unit
                        }
                    })

                comparison_match = re.search(r"Comparison:\s+(\[.*?\])", log_content)
                if comparison_match:
                    if not execution.result:
                        execution.result = []
                    execution.result.append({
                        "additional_info": {
                            "comparison_relaxation": json.loads(comparison_match.group(1))
                        }
                    })

                performance_matches = re.findall(r"#(\w+)\(\.\.\.\):\s+in\s+([\d,.]+)ms", log_content)
                performance_dict = {key: time for key, time in performance_matches}
                if performance_dict:
                    if not execution.result:
                        execution.result = []
                    execution.result.append({
                        "time_execution": performance_dict
                    })

        except Exception as e:
            return None, f"Errore durante il caricamento del file di log: {str(e)}"

        return execution, "Attributi extra"

