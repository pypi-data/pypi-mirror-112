import resource
import sys

from django.core.management import get_commands
from django.core.management.base import CommandError

def getapp(name):
    try:
        return get_commands()[name]
    except KeyError:
        raise CommandError("Unknown command: %r" % name)

def getinstance(command):
    if isinstance(command,str):
        app, name = getapp(command), command
        return load_command_class(app,name)
    return command

def getmemory():
    div = 1024.0 if 'linux' in sys.platform else 1048576.0
    return round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/div,2)
