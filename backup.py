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
            src_files.append((r+'/').lstrip(src + '\\').lstrip(src + '/') + file)

    dst_files = []
    for r, d, f in os.walk(dst):
        for file in f:
            dst_files.append((r+'/').lstrip(dst + '\\').lstrip(dst + '/') + file)

    files_to_process = dst_files.copy()

    for file in src_files:
        if not file in dst_files:
            diff['create'].append(file)
        else:
            if os.path.getmtime(src.replace('.', os.getcwd()) + '/' + file) > os.path.getmtime(dst.replace('.', os.getcwd()) + '/' + file):
                diff['update'].append(file)
            files_to_process.remove(file)

    diff['delete'] = files_to_process

    return diff

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
            os.makedirs(dst.replace('.', os.getcwd()) + '/' + os.path.dirname(file))
        shutil.copy2(src.replace('.', os.getcwd()) + '/' + file, dst.replace('.', os.getcwd()) + '/' + file)
    
    for file in diff['delete']:
        os.remove(dst.replace('.', os.getcwd()) + '/' + file)
    
    return diff

if __name__ == '__main__':
    print(backup('./test/orig', './test/backup'))