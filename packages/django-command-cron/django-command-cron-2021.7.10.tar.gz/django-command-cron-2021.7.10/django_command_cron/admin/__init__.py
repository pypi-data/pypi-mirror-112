from django.contrib import admin

from django_command_cron.models import Call, Command

from .call import CallAdmin
from .command import CommandAdmin

admin.site.register(Call, CallAdmin)
admin.site.register(Command, CommandAdmin)
