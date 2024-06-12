from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as DefaultGroupAdmin
from .models import CustomUser, Group


class GroupAdmin(DefaultGroupAdmin):
    filter_horizontal = ('students',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('users')
        return qs

    def users(self, obj):
        return ", ".join([user.username for user in obj.users.all()])

    users.short_description = 'Студенты'
    list_display = DefaultGroupAdmin.list_display + ('users',)


admin.site.register(Group, GroupAdmin)
admin.site.register(CustomUser)
