from django.contrib import admin
from .models import Desks

@admin.register(Desks)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'description')
