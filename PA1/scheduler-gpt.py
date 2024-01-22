import json
import os

def parse_file(file_name):
    data = {"processes": []}
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
    return data

def main():
    script_dir = os.path.dirname(__file__)  # Get the directory where the script is located
    file_name = os.path.join(script_dir, 'c10-sjf.in')  # Change this to your file name
    data = parse_file(file_name)
    json_data = json.dumps(data, indent=4)
    print(json_data)

if __name__ == "__main__":
    main()
