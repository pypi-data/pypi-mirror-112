from datetime import date
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.timesince import timesince


class CommandAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'args',
        'seconds',
        'is_enabled',
    ]
    list_display = [
        'id',
        'name',
        'args',
        'seconds',
        'run_at',
        'calls',
        'errors',
        'is_enabled',
        'is_running',
        'is_success',
        'started_at_strftime',
        'finished_at_strftime',
        'elapsed',
        'timesince'
    ]
    list_filter = ['seconds','is_enabled','is_running','is_success',]
    readonly_fields = ['is_running','started_at_strftime','finished_at_strftime','elapsed','timesince']
    search_fields = ['name',]

    def calls(self, obj):
        if not obj.calls_count:
            return
        return format_html(
            '<a href="{}">{}</a> ',
            reverse('admin:django_command_cron_call_changelist')+'?name='+obj.name,
            obj.calls_count,
        )
    calls.allow_tags = True
    calls.short_description = 'calls'

    def errors(self, obj):
        if obj.errors_count:
            return format_html(
                '<a href="{}">{}</a> ',
                reverse('admin:django_command_cron_call_changelist')+'?is_success__exact=0&name=%s'+obj.name,
                obj.errors_count,
            )
    errors.allow_tags = True
    errors.short_description = 'errors'

    def started_at_strftime(self,command):
        if command.started_at:
            if command.started_at.date()==date.today():
                return command.started_at.strftime('%H:%M:%S')
            return command.started_at.strftime('%Y-%m-%d %H:%M:%S')
    started_at_strftime.short_description = 'started'

    def finished_at_strftime(self,command):
        if command.finished_at:
            if command.finished_at.date()==date.today():
                return command.finished_at.strftime('%H:%M:%S')
            return command.finished_at.strftime('%Y-%m-%d %H:%M:%S')
    finished_at_strftime.short_description = 'finished'

    def elapsed(self, obj):
        if obj.started_at and obj.finished_at:
            s = str(obj.finished_at - obj.started_at)
            return '.'.join(filter(None,[s.split('.')[0].replace('0:00:00','0'),s.split('.')[1][0:2]]))
    elapsed.short_description = 'elapsed'

    def timesince(self, obj):
        if obj.finished_at:
            return timesince(obj.finished_at).split(',')[0]+' ago'
    timesince.short_description = ''

