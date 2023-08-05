from pathlib import Path

from cvee.fileio.build import FILE_HANDLERS


def load(file, file_format=None, **kwargs):
    """Load data from file of different formats.

    This function provides a unified api for loading data from
    file of different formats.

    Args:
        file (str or Path or fileobj): Filename of a file object.
        file_format (str, optional): Use the file format to specify the
            file handler, otherwise the file format will be inferred from
            the file name. Currently supported file formats: txt, json,
            yaml/yml, csv, pkl/pickle, npy, npz, obj, ply.

    Returns:
        The data of the file.
    """
    if isinstance(file, Path):
        file = str(file)
    if file_format is None and not isinstance(file, str):
        raise TypeError('Format shoud be specified when file is not str or path')
    if file_format is None and isinstance(file, str):
        file_format = file.split('.')[-1]
    if file_format not in FILE_HANDLERS:
        raise TypeError(f'Unsupported file format: {file_format}')

    file_handler = FILE_HANDLERS[file_format]

    if isinstance(file, str):
        obj = file_handler.load_from_path(file, **kwargs)
    elif hasattr(file, 'read'):
        obj = file_handler.load_from_fileobj(file, **kwargs)
    else:
        raise TypeError('File must be a filepath str or a file object')
    return obj
