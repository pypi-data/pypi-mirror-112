from datetime import date
from django.contrib import admin
from django.template.defaultfilters import linebreaksbr
from django.utils.safestring import mark_safe
from django.utils.timesince import timesince

class CallAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'args',
        'is_success',
        'stdout',
        'exc',
        'traceback',
        'started_at_strftime',
        'finished_at_strftime',
        'elapsed',
        'timesince'
    ]
    list_filter = ['name','is_success',]
    search_fields = ['name', ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def exc(self,obj):
        return ': '.join(filter(None,[obj.exc_type,obj.exc_value])) if obj.exc_type else None
    exc.short_description = 'exc'

    def traceback(self,obj):
        return mark_safe(linebreaksbr(obj.exc_traceback)) if obj.exc_traceback else None
    traceback.short_description = 'traceback'

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

    def timesince(self, command):
        if command.finished_at:
            return timesince(command.finished_at).split(',')[0]+' ago'
    timesince.short_description = ''

