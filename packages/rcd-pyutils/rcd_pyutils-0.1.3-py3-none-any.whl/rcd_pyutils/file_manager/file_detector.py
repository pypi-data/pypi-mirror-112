import os
import fnmatch


def detect_path(path, create=False):
    """
        Function detect_path.
        Use this function to detect if a path exsit, if not then create it.

        Parameters:
              path (str): The path of a directory.

        Examples:
            >>> from rcd_pyutils import file_manager
            >>> file_manager.detect_path("my_path")
    """
    if os.path.isdir(path):
        print(f"✓Path \"{path}\" exists.")
    else:
        print(f"Path \"{path}\" does not exist, creating...")
        os.makedirs(path)


def detect_all_files(root, suffix=None):
    lst_files = list()
    for path, subdirs, files in os.walk(root):
        for name in files:
            if suffix:
                if fnmatch(name, suffix):
                    lst_files.append(name)
            else:
                lst_files.append(name)
    return lst_files