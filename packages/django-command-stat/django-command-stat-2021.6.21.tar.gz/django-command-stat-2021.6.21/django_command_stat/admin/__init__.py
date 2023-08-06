from django.contrib import admin

from ..models import Call, Command

from .command import CommandAdmin
from .call import CallAdmin

admin.site.register(Command, CommandAdmin)
admin.site.register(Call, CallAdmin)

