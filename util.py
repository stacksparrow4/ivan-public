import os

from pathlib import Path

def create_dir_if_not_exists(dir_name):
    Path(dir_name).mkdir(parents=True, exist_ok=True)

def write_to_path(fpath, data):
    create_dir_if_not_exists(os.path.dirname(fpath))

    with open(fpath, "w") as f:
        f.write(data)
