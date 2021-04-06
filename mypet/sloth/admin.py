from django.contrib import admin

from . import models


class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'tag', 'last', 'last_year')


class OutcomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'time', 'file')


class PreparationFileAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'file_tag', 'ready_file')


admin.site.register(models.Report, ReportAdmin)
admin.site.register(models.Outcome, OutcomeAdmin)
admin.site.register(models.PreparationFile, PreparationFileAdmin)

admin.site.register(models.UserProfile)
