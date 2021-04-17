from pathlib import Path

image_file_extensions = {
    '.jpg', '.jpeg', '.png', '.webp', '.gif', '.webm', '.svg', '.mkv', '.mp4', '.avif', '.y4m', '.jxl'
}


def get_image_files(directory_path):
    """ @:param directory_path must be str or Path object
        @:returns list of Path file objects """
    path_objects = []
    if type(directory_path) is str:
        path = Path(directory_path)
    elif isinstance(directory_path, Path):
        path = directory_path
    else:
        raise ValueError
    print(str(path))
    for entry in path.iterdir():
        if entry.is_file() and entry.suffix.lower() in image_file_extensions:
            path_objects.append(entry)
    return path_objects


def browse_folder(folder):
    path_dir_objects = []
    path_file_objects = []
    for entry in Path(folder).iterdir():
        if entry.is_file() and entry.suffix.lower() in image_file_extensions:
            path_file_objects.append(entry)
        elif entry.is_dir() and entry.name[0] != '.':
            path_dir_objects.append(entry)
    return (path_dir_objects, path_file_objects)


def browse_current_folder():
    return browse_folder('.')