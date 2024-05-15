from abc import ABC, abstractmethod
from classes.dataset.dataset import Dataset
from classes.algorithm.algorithm import Algorithm
from classes.discovery_info import DiscoveryInfo
from classes.execution_info.execution_info import ExecutionInfo

import math
import os
import pandas as pd
import json
import csv

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
            size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
            i = int(math.floor(math.log(size_in_bytes, 1024))) if size_in_bytes > 0 else 0
            p = math.pow(1024, i)
            s = round(size_in_bytes / p, 2) if size_in_bytes > 0 else 0
            return f"{s} {size_name[i]}"

        try:
            file_name = os.path.basename(datasetFile)

            with open(datasetFile, 'r', newline='') as csvfile:
                sample = csvfile.read(1024)
                dialect = csv.Sniffer().sniff(sample)
                delimiter = dialect.delimiter

            df = pd.read_csv(datasetFile, sep=delimiter, keep_default_na=False, header='infer')
            has_header = not df.columns.equals(pd.RangeIndex(start=0, stop=len(df.columns), step=1))
            column_names = list(df.columns) if has_header else list(range(len(df.columns)))

            null_chars = [char for char in ['', '?'] if df.isin([char]).any().any()]

            dataset = Dataset(
                name=file_name,
                size=format_size(os.path.getsize(datasetFile)),
                format="CSV",
                header=column_names,
                col_number=len(df.columns),
                row_number=len(df),
                separator=delimiter,
                blank_char=", ".join(null_chars) if null_chars else None
            )

            return dataset
        except Exception as e:
            print(f"Error loading dataset: {str(e)}")
            return None


    def loadAlgorithm(self, algorithmFile: str) -> Algorithm:
        try:
            with open(algorithmFile, 'r') as file:
                data = json.load(file)
            algorithm_data = data['algorithm']
            algorithm = Algorithm(
                name=algorithm_data.get('name', None),
                language=algorithm_data.get('language', None),
                platform=algorithm_data.get('platform', None),
                execution_type=algorithm_data.get('execution_type', None)
            )
            return algorithm
        except Exception as e:
            print(f"Si è verificato un errore: {e}")
        return None



    def loadExecutionInfo(self, executionInfoFile: str) -> ExecutionInfo:
        try:
            with open(executionInfoFile, 'r') as file:
                data = json.load(file)
            execution_info_data = data['execution_info']
            execution_info = ExecutionInfo(
                system=execution_info_data.get('system', None),
                execution_command=execution_info_data.get('execution_command', None),
                max_execution_time=execution_info_data.get('max_execution_time', None),
                max_ram_usage=execution_info_data.get('max_ram_usage', None),
                start_time=execution_info_data.get('start_time', None),
                end_time=execution_info_data.get('end_time', None)
            )
            return execution_info
        except Exception as e:
            print(f"Si è verificato un errore: {e}")
        return None



    def loadDiscoveryInfo(self) -> DiscoveryInfo:
        exec = self.loadExecution(self.executionFile)
        dataset = self.loadDataset(self.datasetFile)
        algorithm = self.loadAlgorithm(self.algorithmFile)
        executionInfo = self.loadExecutionInfo(self.executionInfoFile)
        return DiscoveryInfo(dataset, algorithm, executionInfo, exec[0], exec[1])
    