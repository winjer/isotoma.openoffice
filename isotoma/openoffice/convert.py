""" Provide a python interface to execute the unoconv utility, if it's present. """

import os
import random
import subprocess
import logging
import tempfile

from which import which

logger = logging.getLogger("isotoma.openoffice")

class ConvertError(Exception):
    """ Conversion failed for some reason """

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
            subprocess.check_call([unoconv, '-f', format, infilename])
            break
        except subprocess.CalledProcessError, e:
            logger.exception(e)
    else:
        os.unlink(infilename)
        os.rmdir(tempdir)
        raise ConvertError("unoconv failed too many times, see log for details")
    if os.path.exists(outfilename):
        data = open(outfilename).read()
        os.unlink(outfilename)
        os.unlink(infilename)
        os.rmdir(tempdir)
        return data
    else:
        os.unlink(infilename)
        os.rmdir(tempdir)
        raise ConvertError("format could not be converted by open office")
