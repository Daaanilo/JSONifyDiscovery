import os
import json
import argparse
import types

from classes.concrete_loader import ConcreteLoader

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

def main():
    parser = argparse.ArgumentParser(
        prog='jsonifydiscovery.py',
        description='Analizza file e genera in output un file JSON.'
    )
    parser.add_argument('csv_file', help="File CSV.")
    parser.add_argument('log_files', nargs='+', help="File di log.")
    parser.add_argument('-o', '--output', help="Output file JSON.", type=str, default="result.json")
    args = parser.parse_args()

    csv_file = args.csv_file
    log_files = args.log_files

    if not log_files:
        print("Nessun file di log specificato.")
        return

    discovery_infos = []
    for log_file in log_files:
        loader = ConcreteLoader(executionFile=log_file, datasetFile=csv_file, algorithmFile="", executionInfoFile="")
        discovery_info = loader.loadDiscoveryInfo()
        discovery_infos.append(discovery_info)

    save_results_to_json(discovery_infos, args.output)


if __name__ == "__main__":
    main()
