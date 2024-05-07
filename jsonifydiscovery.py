import os
import json
import tkinter as tk
from tkinter import filedialog
from tkinter.simpledialog import askstring
import tkinter.messagebox as messagebox
import re

def format_size(size_in_bytes):
    for unit in ['bytes', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return "{:.1f} {}".format(size_in_bytes, unit)
        size_in_bytes /= 1024.0

def parse_discovery_results(file_path):
    def parse_log(log_content):
        log_dict = {
            "dataset": {
                "name": "",
                "header": [],
                "size": "",
                "format": "",
                "col_number": "",
                "row_number": ""
            },
            "algorithm": {
                "name": "",
                "language": "",
                "platform": "",
                "parameter": {
                    "separator": "",
                    "blank_char": "",
                    "execution_type": ""
                }
            },
            "execution_info": {
                "system": {
                    "os": "",
                    "os_version": "",
                    "processor": "",
                    "thread": "",
                    "core": "",
                    "ram": ""
                },
                "execution_command": "",
                "max_execution_time": "",
                "max_ram_usage": "",
                "start_time": "",
                "end_time": ""
            },
            "execution": {
                "type": "",
                "scenario": "",
                "result": []
            }
        }

        dataset_match = re.search(r"Dataset:\s+(\w+)\.(\w+)", log_content)
        if dataset_match:
            dataset_name = dataset_match.group(1)
            dataset_format = dataset_match.group(2)
            log_dict["dataset"]["name"] = dataset_name
            log_dict["dataset"]["format"] = dataset_format

        comparison_match = re.search(r"Comparison:\s+(\[.*?\])", log_content)
        if comparison_match:
            log_dict["execution"]["result"].append({
                "additional_info": {
                    "comparison_relaxation": json.loads(comparison_match.group(1))
                }
            })

        performance_matches = re.findall(r"#(\w+)\(\.\.\.\):\s+in\s+([\d,.]+)ms", log_content)
        performance_dict = {key: time for key, time in performance_matches}
        if performance_dict:
            log_dict["execution"]["result"].append({
                "time_execution": performance_dict
            })

        rfd_matches = re.findall(r"RFDs:\n(.*?)\n\n", log_content, re.DOTALL)
        if rfd_matches:
            rfd_list = [line.strip() for line in rfd_matches[0].split("\n")]
            if rfd_list:
                log_dict["execution"]["result"].append({
                    "data": [{"cc": rfd} for rfd in rfd_list]
                })

        statistics_match = re.search(r"Used lowerbound:\s+(\d+)\nUsed upperbound:\s+(\d+)\nExact solved:\s+(\d+)\nTime limit:\s+(\w+)\nOut of memory:\s+(\w+)\nMemory consumption:\s+(\d+MB)\nRFDs count:\s+(\d+)", log_content)
        if statistics_match:
            log_dict["execution"]["result"].append({
                "statistics": {
                    "usedLowerbound": int(statistics_match.group(1)),
                    "usedUpperbound": int(statistics_match.group(2)),
                    "exactSolved": int(statistics_match.group(3)),
                    "timeLimit": statistics_match.group(4) == "true",
                    "outOfMemory": statistics_match.group(5) == "true",
                    "memoryConsumption": statistics_match.group(6),
                    "RFDsCount": int(statistics_match.group(7))
                }
            })

        return log_dict

    results = []

    with open(file_path, 'r') as file:
        log_content = file.read()
        parsed_log = parse_log(log_content)

        file_size = os.path.getsize(file_path)
        parsed_log["dataset"]["size"] = format_size(file_size)

        results.append(parsed_log)

    return results


def check_missing_fields(parsed_results):
    missing_fields = []
    for result in parsed_results:
        for key, value in result.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, dict):
                        for sub_sub_key, sub_sub_value in sub_value.items():
                            if sub_sub_value == "":
                                missing_fields.append((key, sub_key, sub_sub_key))
                    elif sub_value == "":
                        missing_fields.append((key, sub_key))
            elif value == "":
                missing_fields.append(key)
    return missing_fields

def fill_missing_fields(parsed_results, missing_fields):
    for field in missing_fields:
        if len(field) == 3:
            key, sub_key, sub_sub_key = field
            user_input = askstring("Valore mancante", f"Inserisci il valore per '{sub_sub_key}' di '{sub_key}' di '{key}': ")
            for result in parsed_results:
                result[key][sub_key][sub_sub_key] = user_input
        elif len(field) == 2:
            key, sub_key = field
            user_input = askstring("Valore mancante", f"Inserisci il valore per '{sub_key}' di '{key}': ")
            for result in parsed_results:
                result[key][sub_key] = user_input
        else:
            key = field[0]
            user_input = askstring("Valore mancante", f"Inserisci il valore per '{key}': ")
            for result in parsed_results:
                result[key] = user_input

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        parsed_results = parse_discovery_results(file_path)
        missing_fields = check_missing_fields(parsed_results)
        if missing_fields:
            fill_missing_fields(parsed_results, missing_fields)
        
        save_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if save_path:
            try:
                with open(save_path, "w") as json_file:
                    json.dump(parsed_results, json_file, indent=4)
                messagebox.showinfo("Successo", "File JSON salvato con successo.")
            except Exception as e:
                messagebox.showerror("Errore", f"Si è verificato un errore durante il salvataggio del file: {str(e)}")

def main():
    root = tk.Tk()
    root.title("Generatore di file JSON")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    label = tk.Label(frame, text="Seleziona il file da leggere:")
    label.grid(row=0, column=0, padx=5, pady=5)

    browse_button = tk.Button(frame, text="Sfoglia", command=browse_file)
    browse_button.grid(row=0, column=1, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
