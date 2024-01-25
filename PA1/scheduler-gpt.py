import json
import os
import sys

def parse_file(file_name):
    data = {
        "processes": [],
        "algorithm": None,
        "quantum": None,
        "processcount": None,
        "runfor": None
    }

    with open(file_name, 'r') as file:
        for line in file:
            if line.startswith('processcount'):
                data['processcount'] = int(line.split()[1])
            elif line.startswith('runfor'):
                data['runfor'] = int(line.split()[1])
            elif line.startswith('use'):
                data['algorithm'] = line.split()[1]
            elif line.startswith('quantum'):
                data['quantum'] = int(line.split()[1])
            elif line.startswith('process'):
                parts = line.split()
                process_data = {
                    "name": parts[2],
                    "arrival": int(parts[4]),
                    "burst": int(parts[6])
                }
                data['processes'].append(process_data)
    
    # Validate required parameters
    if data['processcount'] is None:
        raise ValueError("Error: Missing parameter processcount")
    if data['runfor'] is None:
        raise ValueError("Error: Missing parameter runfor")
    if data['algorithm'] is None:
        raise ValueError("Error: Missing parameter algorithm")
    if data['algorithm'] == 'rr' and data['quantum'] is None:
        raise ValueError("Error: Missing quantum parameter when use is 'rr'")

    return data

def main():
    if len(sys.argv) != 2:
        print("Usage: python scheduler-gpt.py <inputfile.in>")
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(script_dir, sys.argv[1])

    try:
        if not os.path.isfile(file_name):
            print(f"File not found: {file_name}")
            sys.exit(1)

        data = parse_file(file_name)
        json_data = json.dumps(data, indent=4)
        print(json_data)
    except ValueError as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
