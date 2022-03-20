from django.contrib import admin

from . import models


admin.site.site_header = 'SoftDesk'
admin.site.site_title = 'SoftDesk - Interface administrateur'
admin.site.index_title = 'Interface administrateur'


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')


admin.site.register(models.User, UserAdmin)


