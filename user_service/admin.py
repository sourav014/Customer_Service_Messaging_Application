from django.contrib import admin
from .models import User

# Register your models here.


@admin.register(User)
class NotifyAppUpdateAdmin(admin.ModelAdmin):
    fields = (
        'first_name',
        'last_name', 
        'phone', 
        'email',
    )
    list_display = (
        'first_name',
        'last_name', 
        'phone', 
        'email',
    )
