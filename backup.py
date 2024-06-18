# TIny BackUp
# file backup module for python
# 2023, Mizu

import shutil, os

def generate_diff(src: str, dst: str) -> dict:
    """Generate a file diff for the backup system.

    Args:
        src (str): the source folder.
        dst (str): the folder to back up to.

    Returns:
        dict: a dictionary of associations in this format: {
            'create': ['file/in/src/and/not/in/dst', '...'],
            'update': ['file/with/more/recent/timestamp/in/src', '...'],
            'delete': ['file/in/dst/and/not/in/src', '...']
        }
    """

    if not os.path.exists(dst):
        os.makedirs(dst)

    diff = {
        'create': [],
        'update': [],
        'delete': []
    }

    src_files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(src):
        for file in f:
            src_files.append((r+'/').removeprefix(src + '\\').removeprefix(src + '/') + file)

    dst_files = []
    for r, d, f in os.walk(dst):
        for file in f:
            dst_files.append((r+'/').removeprefix(dst + '\\').removeprefix(dst + '/') + file)

    files_to_process = dst_files.copy()

    for file in src_files:
        if not file in dst_files and os.path.isfile(src + '/' + file):
            diff['create'].append(file)
        elif os.path.isfile(src + '/' + file):
            if os.path.getmtime(src + '/' + file) > os.path.getmtime(dst + '/' + file):
                diff['update'].append(file)
            if file in files_to_process: files_to_process.remove(file)

    diff['delete'] = files_to_process

    return diff

def del_dirs(src):
    """Clean up empty directories.

    Args:
        src (str): the source folder.
    """
    for dirpath, _, _ in os.walk(src, topdown=False):  # Listing the files
        if dirpath == src:
            break
        try:
            if len(os.listdir(dirpath)) == 0:
                os.rmdir(dirpath)
        except OSError as ex:
            print(ex)

def backup(src: str, dst: str) -> dict:
    """Back up a folder to another.

    Args:
        src (str): the source folder.
        dst (str): the folder to back up to.

    Returns:
        dict: the operations done while backing up (creations, updates, deletions)
    """
    diff = generate_diff(src, dst)

    for file in diff['create'] + diff['update']:
        if not os.path.exists(dst.replace('.', os.getcwd()) + '/' + os.path.dirname(file)):
            os.makedirs(dst + '/' + os.path.dirname(file))
        shutil.copy2(src + '/' + file, dst + '/' + file)
    
    for file in diff['delete']:
        os.remove(dst + '/' + file)

    # remove empty directories
    del_dirs(dst)
    
    return diff

if __name__ == '__main__':
    print(backup('./test/orig', './test/backup'))