
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from birthday.models import staffDetails


# Add Staff form
class staffDetailsCreateForm(forms.ModelForm):      
    staff_image = forms.ImageField(label='Profile Picture', required=False) 
    
    class Meta: 
        model = staffDetails 
        fields = [
            'first_name', 'middle_name', 'last_name', 'gender', 'phone_number', 'email', 
            'cadre', 'first_appointment', 'department', 'level', 'step', 'staff_image', 
            'birth_month', 'birth_day'
        ]
        
        
# Update Staff form
class staffDetailsUpdateForm(forms.ModelForm):      
    staff_image = forms.ImageField(label='Change Profile Picture', widget=forms.FileInput) 
    
    class Meta: 
        model = staffDetails 
        fields = [
            'first_name', 'middle_name', 'last_name', 'gender', 'phone_number', 'email', 
            'cadre', 'first_appointment', 'department', 'level', 'step', 'staff_image', 
            'birth_month', 'birth_day', 'delete_image'
        ]   