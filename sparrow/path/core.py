from pathlib import Path


def path_rel_to_abs(rel_path, file_path=__file__):
    current_dir = Path(file_path).absolute().parent
    return current_dir.joinpath(rel_path)
