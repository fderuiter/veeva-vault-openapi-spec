import os
import argparse
from ruamel.yaml import YAML

def fix_lint_errors(batch, batch_size):
    paths_dir = 'api/v25.1/paths/'
    yaml_parser = YAML()
    yaml_parser.preserve_quotes = True

    files = [f for f in os.listdir(paths_dir) if f.endswith('.yaml')]
    files.sort()

    start_index = (batch - 1) * batch_size
    end_index = start_index + batch_size
    files_to_process = files[start_index:end_index]

    print(f"Processing batch {batch}: {len(files_to_process)} files (from index {start_index} to {end_index-1})")

    for filename in files_to_process:
        filepath = os.path.join(paths_dir, filename)

        try:
            with open(filepath, 'r') as f:
                data = yaml_parser.load(f)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            continue

        if not data:
            print(f"Skipping empty file: {filepath}")
            continue

        for key, value in data.items():
            if isinstance(value, dict) and key in ['get', 'post', 'put', 'delete', 'patch', 'head', 'options', 'trace']:
                operation = value
                if 'description' not in operation:
                    operation['description'] = 'No description available.'
                if 'operationId' not in operation:
                    base_name = os.path.splitext(filename)[0]
                    operation['operationId'] = f"{base_name}_{key}"
                if 'tags' not in operation:
                    operation['tags'] = ['Default']
                if 'parameters' in operation and operation.get('parameters'):
                    for param in operation['parameters']:
                        if 'schema' in param and 'example' in param:
                            schema_type = param['schema'].get('type')
                            example_val = param['example']
                            if schema_type == 'boolean':
                                if not isinstance(example_val, bool):
                                    if str(example_val).lower() == 'true':
                                        param['example'] = True
                                    else:
                                        param['example'] = False
                            elif schema_type == 'integer':
                                if not isinstance(example_val, int):
                                    try:
                                        param['example'] = int(example_val)
                                    except (ValueError, TypeError):
                                        if 'example' in param:
                                            del param['example']
                            elif isinstance(example_val, bool):
                                param['example'] = str(example_val)
        if 'parameters' in data and data.get('parameters'):
            for param in data['parameters']:
                if 'schema' in param and 'example' in param:
                    schema_type = param['schema'].get('type')
                    example_val = param['example']
                    if schema_type == 'boolean' and not isinstance(example_val, bool):
                        if str(example_val).lower() == 'true':
                            param['example'] = True
                        else:
                            param['example'] = False

        with open(filepath, 'w') as f:
            yaml_parser.dump(data, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fix OpenAPI lint errors in batches.')
    parser.add_argument('--batch', type=int, required=True, help='The batch number to process (1-based).')
    parser.add_argument('--batch-size', type=int, default=50, help='The number of files to process in each batch.')
    args = parser.parse_args()

    fix_lint_errors(args.batch, args.batch_size)
    print(f"Linting errors script finished for batch {args.batch}.")
