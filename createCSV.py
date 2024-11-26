import os
import json
import csv
from icecream import ic

def json_to_csv(json_folder, csv_folder):
    try:
        os.makedirs(csv_folder, exist_ok=True)

        # Iterate through all JSON files in the folder
        for filename in os.listdir(json_folder):
            if filename.endswith(".json"):
                json_file_path = os.path.join(json_folder, filename)
                
                # Read JSON data
                with open(json_file_path, "r") as json_file:
                    data = json.load(json_file)

                # Determine the output CSV filename
                csv_filename = f"{os.path.splitext(filename)[0]}.csv"
                csv_file_path = os.path.join(csv_folder, csv_filename)
                
                # Convert JSON to CSV
                with open(csv_file_path, "w", newline="") as csv_file:
                    if isinstance(data, list) and data:
                        # Collect all unique keys from all dictionaries
                        fieldnames = set()
                        for entry in data:
                            fieldnames.update(entry.keys())
                        fieldnames = list(fieldnames)
                        
                        # Write the CSV header based on all unique keys
                        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(data)
                    else:
                        ic(f"Skipping file {filename}: JSON does not contain a list of dictionaries.")
                
                ic(f"Converted {filename} to {csv_filename}.")
    except Exception as e:
        ic(f"Error while converting JSON to CSV: {e}")

if __name__ == "__main__":
    # Specify the folder containing JSON files and the output folder for CSV files
    json_folder = "./devices_json"
    csv_folder = "./csv"

    # Convert JSON files to CSV
    json_to_csv(json_folder, csv_folder)