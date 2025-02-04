import os
import csv
from icecream import ic

def merge_csv_files(csv_folder, output_file):
    try:
        # List to hold the fieldnames of all CSV files
        fieldnames = set()
        csv_files = [f for f in os.listdir(csv_folder) if f.endswith(".csv")]

        # Collect all unique fieldnames from all CSV files
        for csv_file in csv_files:
            csv_file_path = os.path.join(csv_folder, csv_file)
            with open(csv_file_path, "r") as f:
                reader = csv.DictReader(f)
                fieldnames.update(reader.fieldnames)

        fieldnames = list(fieldnames)

        # Write merged CSV file
        with open(output_file, "w", newline="") as output_csv:
            writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
            writer.writeheader()

            for csv_file in csv_files:
                csv_file_path = os.path.join(csv_folder, csv_file)
                with open(csv_file_path, "r") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        writer.writerow(row)

        ic(f"Merged CSV files into {output_file}")
    except Exception as e:
        ic(f"Error while merging CSV files: {e}")

if __name__ == "__main__":
    # Specify the folder containing CSV files and the output merged CSV file
    csv_folder = "./csv"
    merged_csv_file = "merged_devices.csv"

    # Merge all CSV files into one
    merge_csv_files(csv_folder, merged_csv_file)