from django.contrib import admin

from . import models


class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(models.Skill, SkillAdmin)
admin.site.register(models.Position)
admin.site.register(models.Project)
