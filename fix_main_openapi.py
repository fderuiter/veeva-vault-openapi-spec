import re
from ruamel.yaml import YAML

def fix_main_openapi():
    filepath = 'api/v25.1/openapi.yaml'
    yaml = YAML()
    yaml.preserve_quotes = True

    with open(filepath, 'r') as f:
        data = yaml.load(f)

    if 'tags' not in data:
        data['tags'] = [{'name': 'Default', 'description': 'Default category'}]

    paths = data.get('paths', {})
    new_paths = {}
    for path, path_obj in paths.items():
        # Correct all occurrences of parameter syntax
        new_path = path.replace(':{', '{').replace('{{', '{').replace('}}', '}')

        # Remove trailing slash
        if len(new_path) > 1 and new_path.endswith('/'):
            new_path = new_path.rstrip('/')

        new_paths[new_path] = path_obj

    data['paths'] = new_paths

    with open(filepath, 'w') as f:
        yaml.dump(data, f)

if __name__ == '__main__':
    fix_main_openapi()
    print("Main openapi.yaml fixed.")
