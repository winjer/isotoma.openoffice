
import os
import string

# implementation of which found here http://bugs.python.org/file8185/find_in_path.py
def find_in_path(file, path=None):
    if path is None:
        path = os.environ.get('PATH', '')
    if type(path) is type(''):
        path = string.split(path, os.pathsep)
    return filter(os.path.exists,
                  map(lambda dir, file=file: os.path.join(dir, file), path))

def which(file, mode=os.F_OK | os.X_OK, path=None):
    return filter(lambda path, mode=mode: os.access(path, mode),
                  find_in_path(file, path))


