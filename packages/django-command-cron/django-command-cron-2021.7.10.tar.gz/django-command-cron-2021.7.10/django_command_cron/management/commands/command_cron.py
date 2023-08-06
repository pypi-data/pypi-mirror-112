from datetime import datetime, timedelta
import time

from django.core.management.base import BaseCommand

from ...models import Command as Model
from ...utils import call


class Command(BaseCommand):

    def handle(self, *args, **options):
        qs = Model.objects.all()
        if qs.filter(is_running=True).count():
            qs.filter(is_running=True).update(is_running=False,pid=None)
        while True:
            epoch_time = int(time.time())
            for c in filter(lambda c:c.is_enabled,qs.order_by('id')):
                if c.seconds and (not c.finished_at or c.finished_at<datetime.now()-timedelta(seconds=c.seconds)):
                    call(c)
                if c.run_at and c.run_at>=datetime.now() and (not c.finished_at or c.finished_at<c.run_at):
                    call(c)
            time.sleep(0.01)
            while int(time.time())==epoch_time:
                time.sleep(0.1)
