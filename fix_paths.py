import os
import re

# The directory containing the path files
paths_dir = 'api/v25.1/paths/'

# Iterate over all files in the directory
for filename in os.listdir(paths_dir):
    filepath = os.path.join(paths_dir, filename)
    if os.path.isfile(filepath):
        with open(filepath, 'r') as f:
            content = f.read()

        # Replace {{version}} with {version}
        content = content.replace('{{version}}', '{version}')

        # Also replace the :param syntax with {param}
        content = re.sub(r':({[a-zA-Z0-9_]+})', r'\1', content)

        with open(filepath, 'w') as f:
            f.write(content)

print("Finished fixing paths.")
