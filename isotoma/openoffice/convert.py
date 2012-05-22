""" Provide a python interface to execute the unoconv utility, if it's present. """

import os
import string
import random
import subprocess
import logging
import tempfile

logger = logging.getLogger("isotoma.openoffice")

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

def convert(document, format="pdf", port_range=(23400,23600), tries=3):
    """ Convert the document into the specified format. A random port is
    chosen from the provided port range. Returns a string containing the
    generated file data. """
    locations = which("unoconv", path=os.environ['PATH'])
    if not locations:
        raise KeyError("Cannot find unoconv on search path")
    unoconv = locations[0]
    port = random.randint(*port_range)
    tempdir = tempfile.mkdtemp()
    infilename = os.path.join(tempdir, "INPUT")
    outfilename = os.path.join(tempdir, "INPUT." + format) # wild assumption?
    open(infilename, "w").write(document)
    for t in range(tries):
        # multiple tries, because we might collide on the port
        try:
            output = subprocess.check_output([unoconv, '--timeout=30', '-f', format, '-o', tempdir, infilename])
            logger.info(output)
            break
        except subprocess.CalledProcessError, e:
            logger.exception(e)
    else:
        raise IOError("unoconv failed too many times, see log for details")
    data = open(outfilename).read()
    os.unlink(infilename)
    os.unlink(outfilename)
    os.rmdir(tempdir)
    return data
