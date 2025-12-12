import csv
import json
import sys

def csv_to_json(csv_file, json_file):
    data = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert empty strings to None for JSON
            cleaned_row = {k: (v if v else None) for k, v in row.items()}
            data.append(cleaned_row)
    
    output = {'results': data}
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    
    print(f"Converted {len(data)} rows from {csv_file} to {json_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python csv_to_json.py <input.csv> <output.json>")
        sys.exit(1)
    
    csv_to_json(sys.argv[1], sys.argv[2])

