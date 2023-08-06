from contextlib import redirect_stdout
from datetime import datetime
import io
import logging
import os
import traceback

from django.core.management import call_command
from django.core.management.base import BaseCommand

from django_command_cron.models import Call, Command

def call(command):
    started_at = datetime.now()
    exc_type, exc_value, exc_traceback, stdout = None, None, None, None
    is_success = True
    kwargs = dict(
        calls_count = (command.calls_count or 0)+1,
        is_running=False,
        is_success=is_success,
        started_at=started_at,
        pid=None
    )
    try:
        with io.StringIO() as buf, redirect_stdout(buf):
            args = command.args.split(' ') if command.args else []
            Command.objects.filter(pk=command.pk).update(is_running=True,pid=os.getpid())
            result = call_command(command.name,*args)
            stdout = buf.getvalue()
            return result
    except Exception as e:
        exc_type = '.'.join(filter(None,[type(e).__module__,type(e).__name__]))
        exc_value = str(e)
        exc_traceback = '\n'.join(traceback.format_tb(e.__traceback__))
        is_success = False
        kwargs['errors_count']  = (command.errors_count or 0)+1
        logging.error(e, exc_info=True)
    finally:
        finished_at = datetime.now()
        if stdout:
            print(stdout)
        kwargs['finished_at'] = finished_at
        Command.objects.filter(pk=command.pk).update(**kwargs)
        Call(
            name=command.name,
            args = command.args,
            is_success=is_success,
            started_at=started_at,
            finished_at=finished_at,
            exc_type=exc_type,
            exc_value=exc_value,
            exc_traceback=exc_traceback,
            stdout=stdout
        ).save()


