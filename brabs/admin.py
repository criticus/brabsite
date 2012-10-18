from django.contrib import admin
from brabs.models import Brab

class BrabAdmin(admin.ModelAdmin):
    list_display = ('title', 'auth_user', 'created_at', 'visible', 'deleted')
    list_filter = ('auth_user',)

admin.site.register(Brab, BrabAdmin)
