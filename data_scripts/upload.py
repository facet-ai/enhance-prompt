import os
import csv
import argparse
from datasets import load_dataset
from huggingface_hub import create_repo


# Define a function to convert text files to CSV format
def text_to_csv(file_paths, format_type="default"):
    rows = []
    for file_path in file_paths:
        with open(file_path, "r") as f:
            lines = f.readlines()
        for i in range(0, len(lines) - 1, 3):
            input_line = lines[i].strip()
            output_line = lines[i + 1].strip()
            if format_type == "input_output":
                row = f"[input] {input_line} [output] {output_line}"
            else:
                row = f"{input_line}\n{output_line}"
            rows.append({"text": row})
    return rows


# Initialize argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--dataset-name", type=str, required=True)
parser.add_argument("--resume", action="store_true")
parser.add_argument(
    "--format", type=str, choices=["default", "input_output"], default="default"
)
parser.add_argument("--org", type=str)
args = parser.parse_args()

# Get all file paths in the 'data' directory
file_paths = [os.path.join("data", f) for f in os.listdir("data") if f.endswith(".txt")]

# Convert text files to CSV
csv_rows = text_to_csv(file_paths, args.format)

# Check if dataset file already exists
dataset_file = f"{args.dataset_name}.csv"
if os.path.exists(dataset_file):
    if args.resume:
        dataset = load_dataset("csv", data_files=dataset_file)
    else:
        print(f"Dataset file {dataset_file} already exists.")
        print("Use --resume flag to resume upload.")
        exit(1)
else:
    # [Change] Write to CSV only if it doesn't exist or if --resume flag is not set
    with open(dataset_file, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["text"])
        writer.writeheader()
        writer.writerows(csv_rows)
    dataset = load_dataset("csv", data_files=dataset_file)

# Create repository on Hugging Face


# catch HfHubHTTPError and continue
if not args.org:
    raise ValueError("Please provide an organization name using the --org flag.")

try:
    create_repo(f"{args.org}/{args.dataset_name}")
except Exception as e:
    print(e)


# [Change] Use correct method to upload dataset to Hugging Face
# NOTE: This assumes that your Dataset object has a `push_to_hub` method.
# Please adjust as needed based on your version of the `datasets` library.
dataset["train"].push_to_hub(f"{args.org}/{args.dataset_name}")
