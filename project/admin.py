from django.contrib import admin

from . import models


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'author_user_id')


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'project_id', 'role')


admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Comment)
admin.site.register(models.Issue)
admin.site.register(models.Contributor, ContributorAdmin)




