from django.db import models

class Call(models.Model):
    name = models.CharField(max_length=255)
    args = models.CharField(max_length=255,null=True)

    is_success = models.BooleanField(default=False,verbose_name='success')
    stdout = models.TextField(null=True)

    exc_type = models.TextField(null=True,verbose_name='type')
    exc_value = models.TextField(null=True,verbose_name='value')
    exc_traceback = models.TextField(null=True,verbose_name='traceback')

    started_at = models.DateTimeField()
    finished_at = models.DateTimeField()

    class Meta:
        db_table = 'django_command_cron_call'
        indexes = [
           models.Index(fields=['name',]),
           models.Index(fields=['-started_at',]),
           models.Index(fields=['-finished_at',]),
        ]
        ordering = ('-started_at',)

