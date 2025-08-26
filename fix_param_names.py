import os
import re
import argparse
from ruamel.yaml import YAML

def fix_param_names(batch, batch_size):
    paths_dir = 'api/v25.1/paths/'
    yaml = YAML()
    yaml.preserve_quotes = True

    files = sorted([f for f in os.listdir(paths_dir) if f.endswith('.yaml')])

    start_index = (batch - 1) * batch_size
    end_index = start_index + batch_size
    files_to_process = files[start_index:end_index]

    print(f"Processing batch {batch}: {len(files_to_process)} files from index {start_index} to {end_index-1}")

    for filename in files_to_process:
        filepath = os.path.join(paths_dir, filename)

        try:
            with open(filepath, 'r') as f:
                data = yaml.load(f)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            continue

        if not data:
            continue

        def correct_names(parameters):
            if parameters:
                for param in parameters:
                    if 'name' in param and isinstance(param['name'], str):
                        param['name'] = param['name'].strip('{}')

        if 'parameters' in data:
            correct_names(data['parameters'])

        for op_key, operation in data.items():
            if op_key in ['get', 'post', 'put', 'delete', 'patch', 'head', 'options', 'trace'] and isinstance(operation, dict):
                if 'parameters' in operation:
                    correct_names(operation['parameters'])

        with open(filepath, 'w') as f:
            yaml.dump(data, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fix OpenAPI parameter name errors in batches.')
    parser.add_argument('--batch', type=int, required=True, help='The batch number to process (1-based).')
    parser.add_argument('--batch-size', type=int, default=50, help='The number of files to process in each batch.')
    args = parser.parse_args()

    fix_param_names(args.batch, args.batch_size)
    print(f"Parameter name fixing script finished for batch {args.batch}.")
