import pandas as pd
import sys
import os
import json
from openpyxl.utils import column_index_from_string

# Excel columns you want
COLUMN_RANGES = [
    "C",
    "K", "L", "M",
    "O",
    "T",
    "W", "X",
    "Z",
    "AB", "AC", "AD", "AE", "AF", "AG",
    "AH:AM",
    "AT", "AU", "AV",
    "IO",
    "IR",
    "IS:IX",
    "IY:JF",
    "JG:JK",
    "JN:JO",
    "JZ:KB",
    "KW",
    "LC"
]

def expand_columns(ranges):
    cols = []

    for item in ranges:
        if ":" in item:
            start, end = item.split(":")
            start_idx = column_index_from_string(start)
            end_idx = column_index_from_string(end)

            for i in range(start_idx, end_idx + 1):
                cols.append(i - 1)  # pandas uses 0-based indexing
        else:
            cols.append(column_index_from_string(item) - 1)

    return sorted(set(cols))

def xlsx_to_json(input_file, output_file=None):
    # Read entire sheet
    df = pd.read_excel(input_file)

    # Select only desired columns
    selected_cols = expand_columns(COLUMN_RANGES)
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