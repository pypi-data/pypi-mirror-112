from django.db import models

class Call(models.Model):
    app = models.TextField()
    name = models.TextField()
    sys_argv = models.TextField(null=True,verbose_name='sys.argv')
    args = models.TextField(null=True)
    options = models.TextField(null=True)

    is_success = models.BooleanField(verbose_name='success')
    stdout = models.TextField(null=True)
    hostname = models.TextField(null=True)
    cpu_time = models.FloatField(default=0.00)
    mem_before = models.FloatField(verbose_name='mem before')
    mem_after = models.FloatField(verbose_name='mem after')
    queries_count = models.TextField(verbose_name='queries')

    exc_type = models.TextField(null=True)
    exc_value = models.TextField(null=True)
    exc_traceback = models.TextField(null=True)

    started_at = models.DateTimeField(verbose_name='started')
    finished_at = models.DateTimeField(verbose_name='finished')

    class Meta:
        db_table = 'django_command_stat_call'
        indexes = [
           models.Index(fields=['app',]),
           models.Index(fields=['name',]),
           models.Index(fields=['is_success',]),
           models.Index(fields=['exc_type',]),
           models.Index(fields=['-started_at',]),
        ]
        ordering = ('-started_at',)
