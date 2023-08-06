from datetime import date
from django.contrib import admin
from django.template.defaultfilters import linebreaksbr
from django.utils.timesince import timesince

class CallAdmin(admin.ModelAdmin):
    list_display = ['id','name','sys_argv','args','options_linebreaksbr','is_success','exc','stdout_linebreaksbr','queries_count','elapsed','mem','cpu_time','hostname','started_at_strftime','finished_at_strftime','timesince']
    list_filter = ('app', 'name', 'is_success','hostname','exc_type')
    search_fields = ('app', 'name',)

    def mem(self,obj):
        return '%s - %s' % (obj.mem_before,obj.mem_after,)
    mem.short_description = 'mem'

    def options_linebreaksbr(self,e):
        return linebreaksbr(e.options) if e.options else None
    options_linebreaksbr.allow_tags = True
    options_linebreaksbr.short_description = 'options'

    def stdout_linebreaksbr(self,e):
        return linebreaksbr(e.stdout) if e.stdout else None
    stdout_linebreaksbr.allow_tags = True
    stdout_linebreaksbr.short_description = 'output'

    def exc(self,e):
        return ': '.join(filter(None,[e.exc_type,e.exc_value])) if e.exc_type else None
    exc.short_description = 'exc'

    def traceback(self,e):
        return linebreaksbr(e.exc_traceback) if e.exc_traceback else None
    traceback.allow_tags = True
    traceback.short_description = 'traceback'

    def started_at_strftime(self, obj):
        if obj.started_at:
            datetime_format = '%H:%M:%S' if obj.started_at.date()==date.today() else '%Y-%m-%d'
            return obj.started_at.strftime(datetime_format)
    started_at_strftime.short_description = 'started'

    def finished_at_strftime(self, obj):
        if obj.started_at:
            datetime_format = '%H:%M:%S' if obj.started_at.date()==date.today() else '%Y-%m-%d'
            return obj.started_at.strftime(datetime_format)
    finished_at_strftime.short_description = 'finished'

    def elapsed(self, obj):
        if obj.started_at and obj.finished_at:
            s = str(obj.finished_at - obj.started_at)
            return '.'.join(filter(None,[s.split('.')[0].replace('0:00:00','0'),s.split('.')[1][0:2]]))
    elapsed.short_description = 'elapsed'

    def timesince(self, obj):
        if obj.started_at:
            return timesince(obj.started_at).split(',')[0]+' ago' if obj.started_at else None
    timesince.short_description = ''

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
