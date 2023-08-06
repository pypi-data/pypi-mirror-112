from django.db import models

class Command(models.Model):
    app = models.TextField()
    name = models.TextField(unique=True)

    is_success = models.BooleanField(null=True,verbose_name='success')
    is_running = models.BooleanField(null=True,verbose_name='running')
    pid = models.IntegerField(null=True)
    cpu_time = models.FloatField(null=True)
    mem_before = models.FloatField(null=True,verbose_name='mem before')
    mem_after = models.FloatField(null=True,verbose_name='mem after')

    calls_count = models.IntegerField(default=1,verbose_name='calls')
    errors_count = models.IntegerField(default=0,verbose_name='errors')

    started_at = models.DateTimeField(null=True,verbose_name='started')
    finished_at = models.DateTimeField(null=True,verbose_name='finished')

    class Meta:
        db_table = 'django_command_stat_command'
        indexes = [
           models.Index(fields=['app',]),
           models.Index(fields=['name',]),
           models.Index(fields=['is_running',]),
           models.Index(fields=['is_success',]),
           models.Index(fields=['-finished_at',]),
        ]
        ordering = ('name',)
