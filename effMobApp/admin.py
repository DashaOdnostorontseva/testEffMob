from django.contrib import admin
from .models import Users, Roles, UserRoles, Passwords, EntryMonitoring

admin.site.register(Users)
admin.site.register(Roles)
admin.site.register(UserRoles)
admin.site.register(Passwords)
admin.site.register(EntryMonitoring)