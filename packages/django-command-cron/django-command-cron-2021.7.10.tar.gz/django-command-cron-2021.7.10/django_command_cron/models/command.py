from django.db import models

class Command(models.Model):
    name = models.CharField(max_length=255)
    args = models.CharField(max_length=255,null=True,blank=True)
    seconds = models.IntegerField()
    pid = models.IntegerField(null=True)

    calls_count = models.IntegerField(null=True,verbose_name='calls')
    errors_count = models.IntegerField(null=True)

    is_enabled = models.BooleanField(null=True,verbose_name='enabled')
    is_running = models.BooleanField(null=True,verbose_name='running')
    is_success = models.BooleanField(null=True,verbose_name='success')

    run_at = models.DateTimeField(null=True)
    started_at = models.DateTimeField(null=True,verbose_name='started')
    finished_at = models.DateTimeField(null=True,verbose_name='finished')

    class Meta:
        db_table = 'django_command_cron_command'
        indexes = [
           models.Index(fields=['name',]),
           models.Index(fields=['is_enabled',]),
           models.Index(fields=['is_running',]),
           models.Index(fields=['is_success',]),
        ]
