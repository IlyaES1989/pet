from django.contrib import admin
from . import models


class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'tag')

class OutcomeAdmin(admin.ModelAdmin):
    list_display = ('time', 'report', 'filename')


admin.site.register(models.Report, ReportAdmin)
admin.site.register(models.Outcome, OutcomeAdmin)
admin.site.register(models.Variable)
admin.site.register(models.UserProfile)
