from django.contrib import admin
from .models import Student
from .models import Notes
from .models import Semester
from .models import Subject
from .models import Topic
from .models import Sheets
from .models import Mcq
from .models import Link

# Register your models here.

# Simple registration
admin.site.register(Student)
admin.site.register(Notes)
admin.site.register(Semester)
admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(Sheets)
admin.site.register(Mcq)
admin.site.register(Link)

from django.contrib import admin
from django.contrib.admin.models import LogEntry

class LogEntryAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_bulk_delete_permission(self, request, obj=None):
        return False

try:
    admin.site.unregister(LogEntry)
except admin.sites.NotRegistered:
    pass

admin.site.register(LogEntry, LogEntryAdmin)
