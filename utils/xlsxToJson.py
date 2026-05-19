import pandas as pd
import sys
import os
import json
from openpyxl.utils import column_index_from_string

# Define exclusion range (V:LC)
EXCLUDE_RANGE = ("V", "LC")

def expand_columns(total_cols, exclude_range):
    start_idx = column_index_from_string(exclude_range[0]) - 1
    end_idx   = column_index_from_string(exclude_range[1]) - 1

    # Keep all columns except those in the exclusion range
    return [i for i in range(total_cols) if not (start_idx <= i <= end_idx)]

def xlsx_to_json(input_file, output_file=None):
    # Read entire sheet
    df = pd.read_excel(input_file)

    # Get total number of columns
    total_cols = df.shape[1]

    # Select only desired columns (excluding V:LC)
    selected_cols = expand_columns(total_cols, EXCLUDE_RANGE)
    df = df.iloc[:, selected_cols]

    # Convert to records
    data = df.to_dict(orient="records")

    # Output filenames
    if output_file is None:
        base, _ = os.path.splitext(input_file)
        output_file = base + ".json"
    csv_file = os.path.splitext(output_file)[0] + ".csv"

    # Save JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    # Save CSV
    df.to_csv(csv_file, index=False, encoding="utf-8")

    print(f"Converted {input_file} → {output_file} and {csv_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python xlsx_to_json.py <input.xlsx> [output.json]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    xlsx_to_json(input_file, output_file)