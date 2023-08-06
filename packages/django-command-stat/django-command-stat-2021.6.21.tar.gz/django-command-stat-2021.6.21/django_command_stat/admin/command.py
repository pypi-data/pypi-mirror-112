from datetime import date
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.timesince import timesince

class CommandAdmin(admin.ModelAdmin):
    list_display = ['id','app','name','calls','errors','is_running', 'pid','is_success','elapsed','mem','cpu_time','strftime','timesince']
    list_filter = ('app', 'name', 'is_running', 'is_success',)
    search_fields = ('app', 'name',)

    def calls(self, obj):
        if obj.calls_count:
            return format_html(
                '<a href="{}">{}</a> ',
                reverse('admin:django_command_stat_call_changelist')+'?name='+obj.name,
                obj.calls_count,
            )
    calls.allow_tags = True
    calls.short_description = 'calls'

    def errors(self, obj):
        if not obj.errors_count:
            return
        return format_html(
            '<a href="{}">{}</a> ',
            reverse('admin:django_command_stat_call_changelist')+'?is_success__exact=0&name=%s'+obj.name,
            obj.errors_count,
        )
    errors.allow_tags = True
    errors.short_description = 'errors'

    def mem(self,obj):
        if obj.mem_before and obj.mem_after:
            return '%s - %s' % (obj.mem_before,obj.mem_after,)
    mem.short_description = 'mem'

    def strftime(self, obj):
        if obj.started_at:
            datetime_format = '%H:%M:%S' if obj.started_at.date()==date.today() else '%Y-%m-%d'
            return obj.started_at.strftime(datetime_format)
    strftime.short_description = 'finished'

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

