import os
import re
import argparse
from ruamel.yaml import YAML

def fix_path_parameters(batch, batch_size):
    main_openapi_file = 'api/v25.1/openapi.yaml'
    paths_dir = 'api/v25.1/paths/'

    yaml = YAML()
    yaml.preserve_quotes = True

    with open(main_openapi_file, 'r') as f:
        main_spec = yaml.load(f)

    path_to_file_map = {path: details['$ref'] for path, details in main_spec.get('paths', {}).items()}

    # Create a reverse map from file to path
    file_to_path_map = {v: k for k, v in path_to_file_map.items()}

    files = sorted(file_to_path_map.keys())

    start_index = (batch - 1) * batch_size
    end_index = start_index + batch_size
    files_to_process = files[start_index:end_index]

    print(f"Processing batch {batch}: {len(files_to_process)} files from index {start_index} to {end_index-1}")

    for file_ref in files_to_process:
        filepath = os.path.join('api/v25.1', file_ref)
        path_string = file_to_path_map.get(file_ref)

        if not path_string:
            print(f"Warning: No path found for file {file_ref}")
            continue

        expected_params = set(re.findall(r'\{(\w+)\}', path_string))

        try:
            with open(filepath, 'r') as f:
                data = yaml.load(f)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            continue

        if not data:
            continue

        # Get params defined at the path level
        path_level_params = {p['name'] for p in data.get('parameters', []) if p.get('in') == 'path'}

        for op_key, operation in data.items():
            if op_key in ['get', 'post', 'put', 'delete', 'patch', 'head', 'options', 'trace'] and isinstance(operation, dict):
                if 'parameters' not in operation or not operation['parameters']:
                    operation['parameters'] = []

                op_params = {p['name'] for p in operation.get('parameters', []) if p.get('in') == 'path'}

                missing_params = expected_params - op_params - path_level_params

                for param_name in missing_params:
                    operation['parameters'].append({
                        'name': param_name,
                        'in': 'path',
                        'required': True,
                        'description': f'The {param_name} parameter.',
                        'schema': {'type': 'string'}
                    })

        with open(filepath, 'w') as f:
            yaml.dump(data, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fix OpenAPI path parameter errors in batches.')
    parser.add_argument('--batch', type=int, required=True, help='The batch number to process (1-based).')
    parser.add_argument('--batch-size', type=int, default=50, help='The number of files to process in each batch.')
    args = parser.parse_args()

    fix_path_parameters(args.batch, args.batch_size)
    print(f"Path parameter script finished for batch {args.batch}.")
