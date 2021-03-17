from django.contrib import admin
from . import models


class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'tag', 'last', 'last_year')

class OutcomeAdmin(admin.ModelAdmin):
    list_display = ('user','report', 'time', 'file')

class PreapationFileAdmin(admin.ModelAdmin):
    list_display = ('user','item', 'tage_file', 'primarily_file', 'ready_file' )


admin.site.register(models.Report, ReportAdmin)
admin.site.register(models.Outcome, OutcomeAdmin)
admin.site.register(models.PreparationFile, PreapationFileAdmin)

admin.site.register(models.UserProfile)
