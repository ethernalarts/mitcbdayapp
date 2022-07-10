from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import staffDetails


class staffDetailsUpdateForm(forms.ModelForm):      
    staff_image = forms.ImageField(label='Profile Picture', widget=forms.FileInput) 
    
    class Meta: 
        model = staffDetails 
        fields = [
            'first_name', 'middle_name', 'last_name', 'gender', 'phone_number', 'email', 
            'cadre', 'first_appointment', 'department', 'level', 'step', 'staff_image', 
            'birth_month', 'birth_day'
        ]   
    
    # first_name = forms.CharField(label='First Name', required=True)
    # last_name = forms.CharField(label='Last Name', required=True)
    # subject = forms.CharField(label='Subject', max_length=100)
    # from_ = forms.EmailField(label='Email', required=True)    
    # message = forms.CharField(widget=forms.Textarea)
    # cc_myself = forms.BooleanField(label='cc_myself', required=False)