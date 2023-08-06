from contextlib import redirect_stdout
from datetime import datetime
import io
import os
from socket import gethostname
import sys
import time
import traceback

from django.core.management import get_commands
from django.core.management.base import CommandError
from django.db import connection
from django.db.models import F

from .models import Call, Command
from .utils import getinstance, getmemory

def command_stat(f):
    def wrapper(command,*args,**options):
        instance = getinstance(command)
        module_name = type(instance).__module__
        app, name = module_name.split('.')[-4], module_name.split('.')[-1]
        exc_type, exc_value, exc_traceback = None, None, None
        is_success = True
        stdout = None
        started_at = datetime.now()
        _cpu_time = time.process_time()
        _queries_count = len(connection.queries)
        mem_before = getmemory()
        kwargs = dict(
            calls_count=F("calls_count") + 1
        )
        try:
            defaults = {'app':app,'is_running':True,'is_success':False,'pid':os.getpid()}
            obj, created = Command.objects.get_or_create(defaults,name=name)
            with io.StringIO() as buf, redirect_stdout(buf):
                result = f(instance,*args, **options)
                stdout = buf.getvalue()
                return result
        except Exception as e:
            exc_type = '.'.join(filter(None,[type(e).__module__,type(e).__name__]))
            exc_value = str(e)
            exc_traceback = '\n'.join(traceback.format_tb(e.__traceback__))
            is_success = False
            kwargs['errors_count'] = F("errors_count") + 1
            raise e
        finally:
            cpu_time = round(time.process_time() - _cpu_time,4)
            mem_after = getmemory()
            if stdout:
                print(stdout)
            queries_count = len(connection.queries) - _queries_count
            finished_at = datetime.now()
            kwargs.update(
                started_at=started_at,
                finished_at=finished_at,
                is_running=False,
                is_success=is_success,
                pid=None,
                cpu_time=cpu_time,
                mem_before=mem_before,
                mem_after=mem_after
            )
            Command.objects.filter(name=name).update(**kwargs)
            Call(
                name=name,
                app=app,
                sys_argv = ' '.join(sys.argv),
                args = ' '.join(args) if args else None,
                options = "\n".join(sorted(
                    map(lambda kv:'%s=%s' % (kv[0],kv[1]),filter(lambda kv:kv[1]!=None,options.items()))
                )),
                is_success=is_success,
                hostname = gethostname(),
                cpu_time=cpu_time,
                mem_before=mem_before,
                mem_after=mem_after,
                queries_count = queries_count,
                started_at=started_at,
                finished_at=finished_at,
                exc_type=exc_type,
                exc_value=exc_value,
                exc_traceback=exc_traceback,
                stdout=stdout
            ).save()
    return wrapper if f else None
