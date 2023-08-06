from __future__ import print_function

import os


# not include files in subdirectories
def get_files_from_dir(dir_path, fullpath=True):
    result = []
    for (_dir, dir_names, filenames) in os.walk(dir_path):
        if not os.path.samefile(_dir, dir_path):
            break
        for filename in filenames:
            if fullpath:
                result.append(os.path.join(_dir, filename))
            else:
                result.append(filename)
    return result


if __name__ == '__main__':
    print(get_files_from_dir('/Users/clpsz/workspace/database-scripts-ng'))
