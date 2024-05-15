import os
import json
import argparse
import types
import importlib

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, types.MappingProxyType):
            return dict(obj)
        elif hasattr(obj, '__json__') and callable(obj.__json__):
            return obj.__json__()
        elif hasattr(obj, '__dict__'):
            filtered_dict = {k: v for k, v in obj.__dict__.items() if not callable(v)}
            return filtered_dict
        else:
            return super().default(obj)

def format_size(size_in_bytes):
    for unit in ['bytes', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return "{:.1f} {}".format(size_in_bytes, unit)
        size_in_bytes /= 1024.0

def save_results_to_json(discovery_infos, save_path):
    try:
        with open(save_path, "w") as json_file:
            json.dump(discovery_infos, json_file, indent=4, cls=CustomJSONEncoder)
        print("File JSON salvato con successo.")
    except Exception as e:
        print(f"Si è verificato un errore durante il salvataggio del file: {str(e)}")

def load_json_file(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Errore durante il caricamento del file JSON {file_path}: {str(e)}")
        return None

def main():
    parser = argparse.ArgumentParser(
        prog='jsonifydiscovery.py',
        description='Analizza file e genera in output un file JSON.'
    )
    parser.add_argument('-d', '--csv_file', help="File CSV.", required=True)
    parser.add_argument('-f', '--log_files', nargs='+', help="File di log.", required=True)
    parser.add_argument('-o', '--output', help="Output file JSON.", type=str, default="result.json")
    parser.add_argument('-a', '--algorithmFile', help="File dell'algoritmo JSON.", type=str)
    parser.add_argument('-e', '--executionInfoFile', help="File di informazioni sull'esecuzione JSON.", type=str)
    parser.add_argument('-l', '--loaderClass', help="Nome della classe del loader.", type=str, required=True)
    args = parser.parse_args()

    csv_file = args.csv_file
    log_files = args.log_files
    algorithm_data = args.algorithmFile
    execution_info_data = args.executionInfoFile
    loader_class_name = args.loaderClass

    module_name, class_name = loader_class_name.rsplit('.', 1)
    try:
        module = importlib.import_module(module_name)
        loader_class = getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        print(f"Errore durante il caricamento della classe {loader_class_name}: {e}")
        return

    discovery_infos = []
    for log_file in log_files:
        loader = loader_class(
            executionFile=log_file, 
            datasetFile=csv_file, 
            algorithmFile=algorithm_data, 
            executionInfoFile=execution_info_data
        )
        discovery_info = loader.loadDiscoveryInfo()
        discovery_infos.append(discovery_info)

    save_results_to_json(discovery_infos, args.output)

if __name__ == "__main__":
    main()
