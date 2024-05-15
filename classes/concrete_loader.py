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
        output = []
        with open(resultFile, 'r') as file:
            for line in file:
                line = line.strip()
                match = re.match(r'([^->]+)\s*->\s*(.*)', line)
                if match:
                    lhs = match.group(1).split('\t')
                    rhs = match.group(2).split('@')
                    data = {"lhs": [], "rhs": {}}
                    
                    for item in lhs:
                        if '@' in item:
                            column, value = item.split('@')
                            data["lhs"].append({"column": column.strip(), "comparison_relaxation": float(value)})
                    
                    if len(rhs) == 2:
                        column = rhs[0].strip()
                        value = rhs[1]
                        data["rhs"] = {"column": column, "comparison_relaxation": float(value)}
                    
                    output.append(data)
            log_content = file.read()

        execution.result = output

        #print(json.dumps(output, indent=4))

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

        return execution, "Attributi extra"

