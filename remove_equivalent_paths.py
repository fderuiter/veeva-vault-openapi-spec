import os
from ruamel.yaml import YAML

def remove_equivalent_paths():
    files_to_delete = [
        'api/v25.1/paths/api_version_configuration_component_type_and_record_name_2a74f1.yaml',
        'api/v25.1/paths/api_version_configuration_object_name_and_object_type_dde89f.yaml',
        'api/v25.1/paths/api_version_objects_binders_binder_id_sections_node_id_eaf5fc.yaml',
        'api/v25.1/paths/api_version_objects_users_user_id_273417.yaml',
        'api/v25.1/paths/api_version_query_previous_page_44e832.yaml',
        'api/v25.1/paths/api_version_objects_sandbox_name_36c5db.yaml'
    ]

    # Delete the files
    for f in files_to_delete:
        if os.path.exists(f):
            os.remove(f)
            print(f"Deleted file: {f}")

    # Remove references from openapi.yaml
    main_openapi_file = 'api/v25.1/openapi.yaml'
    yaml = YAML()
    yaml.preserve_quotes = True

    with open(main_openapi_file, 'r') as f:
        main_spec = yaml.load(f)

    paths = main_spec.get('paths', {})
    paths_to_remove = []

    # Convert file paths to the format used in $ref
    refs_to_delete = ['./' + os.path.relpath(f, 'api/v25.1').replace(os.path.sep, '/') for f in files_to_delete]

    for path, details in paths.items():
        if details.get('$ref') in refs_to_delete:
            paths_to_remove.append(path)

    for path in paths_to_remove:
        del paths[path]
        print(f"Removed path from openapi.yaml: {path}")

    with open(main_openapi_file, 'w') as f:
        yaml.dump(main_spec, f)

if __name__ == '__main__':
    remove_equivalent_paths()
    print("Equivalent paths removed.")
