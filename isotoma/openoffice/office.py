
import os
import uno
import subprocess
import time
import logging
from which import which

logger = logging.getLogger("isotoma.openoffice")

class Office(object):
    
    """ Launch an openoffice background process and use it. Will reconnect to
    an existing process if necessary. NB: you will leave an openoffice
    process lying around after this terminates! """

    server_args = ['--norestore',
                   '--nofirstwizard',
                   '--nologo',
                   '--headless']

    def __init__(self, name="isotoma.openoffice"):
        """ The name is used to uniquely identify this instance """
        self.name = name
        self.subprocess = None
        self.run_openoffice()
        # get the uno component context from the PyUNO runtime
        localContext = uno.getComponentContext()
        # create the UnoUrlResolver
        resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext )
        ctx = resolver.resolve( "uno:%sStarOffice.ComponentContext" % self.pipe_name)
        smgr = ctx.ServiceManager
        self.desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)

    @property  
    def pipe_name(self):
        return "pipe,name=%s;urp;" % (self.name,)
            
    def run_openoffice(self):
        """ Launches openoffice and returns the name of the connection string to it """
        command = [self.office_path, "--accept=%s" % self.pipe_name] + self.server_args
        self.subprocess = subprocess.Popen(command, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
        time.sleep(1)
        self.subprocess.poll()
        
    def load(self, path):
        return self.desktop.loadComponentFromURL("file://" + path, "_blank", 0, ())

    @property
    def office_path(self):
        path = os.environ['PATH']
        office = which('ooffice', path=path)
        if not office:
            office = which('soffice', path=path)
        if not office:
            raise KeyError("Cannot find OpenOffice on path")
        return office[0]

    def document_properties(self, path):
        properties = {}
        doc = self.load(path)
        if doc:
            props = doc.getDocumentProperties().getUserDefinedProperties()
            properties = dict([(x.Name, x.Value) for x in props.getPropertyValues()])
            doc.close(0)
        return properties
