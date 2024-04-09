from django.contrib import admin
from staffapp.models import staffDetails

# Register your models here.


# Register the Admin classes for staffDetails using the decorator
@admin.register(staffDetails)
class staffDetailsAdmin(admin.ModelAdmin):
    
    list_display = ('last_name', 'first_name', 'middle_name', 'official_email', 'date_of_birth')
    list_filter = ('date_of_birth',)
