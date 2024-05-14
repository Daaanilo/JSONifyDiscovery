from abc import ABC, abstractmethod
from classes.dataset.dataset import Dataset
from classes.algorithm.algorithm import Algorithm
from classes.discovery_info import DiscoveryInfo
from classes.execution_info.execution_info import ExecutionInfo

import math
import os
import pandas as pd


class AbstractLoader(ABC):
    executionFile: str
    datasetFile: str
    algorithmFile: str
    executionInfoFile: str

    def __init__(self, executionFile:str,  datasetFile: str, algorithmFile: str, executionInfoFile: str = None):
        self.datasetFile = datasetFile
        self.algorithmFile = algorithmFile
        self.executionInfoFile = executionInfoFile
        self.executionFile = executionFile

    @abstractmethod
    def loadExecution(self, resultFile: dict) -> (ExecutionInfo, str):
        #str extra map
        #metodo che verrà implementato dai vari caricatori per i differenti tipi di file
        pass

    def loadDataset(self, datasetFile: str) -> Dataset:
        def format_size(size_in_bytes):
            if size_in_bytes == 0:
                return "0B"
            size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
            i = int(math.floor(math.log(size_in_bytes, 1024)))
            p = math.pow(1024, i)
            s = round(size_in_bytes / p, 2)
            return "%s %s" % (s, size_name[i])

        try:
            file_name = os.path.basename(datasetFile)

            df = pd.read_csv(datasetFile, iterator=True, keep_default_na=False, sep=None, header=None, engine='python')
            delimiter = df._engine.data.dialect.delimiter
            df = df.read()

            null_chars = ['', '?']
            founded_null_chars = []
            for char in null_chars:
                if char in df.values:
                    founded_null_chars.append(char if char != '' else 'blank')

            columns = len(df.columns)
            rows = len(df)
            initial_type = df.dtypes
            types_without_first_row = df.dtypes
            probably_header = list(initial_type) != list(types_without_first_row)

            dataset = Dataset(
                name=file_name,
                size=format_size(os.path.getsize(datasetFile)),
                format="CSV",
                header=probably_header,
                col_number=columns,
                row_number=rows,
                separator=delimiter,
                blank_char=None if len(founded_null_chars) == 0 else ", ".join(founded_null_chars)
            )

            return dataset
        except Exception as e:
            print(f"Error loading dataset: {str(e)}")
            return None

    def loadAlgorithm(self) -> Algorithm:
        algorithm = Algorithm(
            name=None,
            language=None,
            platform=None,
            execution_type=None
        )
        
        return algorithm


    def loadExecutionInfo(self) -> ExecutionInfo:
        execution_info = ExecutionInfo(
            system=None,
            execution_command=None,
            max_execution_time=None,
            max_ram_usage=None,
            start_time=None,
            end_time=None
        )

        return execution_info

    def loadDiscoveryInfo(self) -> DiscoveryInfo:
        exec = self.loadExecution(self.executionFile)
        dataset = self.loadDataset(self.datasetFile)
        algorithm = self.loadAlgorithm()
        executionInfo = self.loadExecutionInfo()
        return DiscoveryInfo(dataset, algorithm, executionInfo, exec[0], exec[1])
    