from django.contrib import admin
from .models import staffDetails

# Register your models here.


# Register the Admin classes for Book using the decorator
@admin.register(staffDetails)
class staffDetailsAdmin(admin.ModelAdmin):
    
    list_display = ('last_name', 'first_name', 'email', 'birth_month', 'birth_day')
    list_filter = ('birth_month', 'birth_day')
