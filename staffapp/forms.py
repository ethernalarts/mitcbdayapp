
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from birthday.models import staffDetails


# Add Staff form
class staffDetailsCreateForm(forms.ModelForm):
    first_appointment = forms.DateField(label="Date of First Appointment", widget=forms.DateInput(attrs={'type': 'date'}))
    level = forms.IntegerField(label="Grade Level", min_value=1, max_value=17)
    
    class Meta: 
        model = staffDetails 
        fields = [
            'first_name', 'middle_name', 'last_name', 'gender', 'phone_number', 'email', 
            'cadre', 'first_appointment', 'department', 'level', 'step', 'staff_image', 
            'birth_month', 'birth_day'
        ]
    
    # validate email domain name
    def clean_email(self):
        data = self.cleaned_data['email']
        domain = data.split('@')[1]
        domain_list = ["edostate.gov.ng"]
        
        if domain not in domain_list:
            raise ValidationError("Please provide your official email address")
        return data   
    
    # validate image format
    def clean_staff_image(self):
        data = self.cleaned_data['staff_image']
        filetype = data.split('.')[1]
        filetype_list = ["png", "jpg", "jpeg", "gif"]
        
        if filetype not in filetype_list:
            raise forms.ValidationError("Please upload a JPG, PNG or GIF file only")
        return data
        
        
# Update Staff form
class staffDetailsUpdateForm(forms.ModelForm):      
    staff_image = forms.ImageField(label='Change Profile Picture', widget=forms.FileInput, required=False)
    level = forms.IntegerField(label="Grade Level", min_value=1, max_value=17)
    #delete_image = forms.BooleanField()
    
    class Meta: 
        model = staffDetails 
        fields = [
            'first_name', 'middle_name', 'last_name', 'gender', 'phone_number', 'email', 
            'cadre', 'first_appointment', 'department', 'level', 'step', 'staff_image', 
            'birth_month', 'birth_day', 'delete_image'
        ]   
    
    # validate email domain name
    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('@')[1]
        domain_list = ["edostate.gov.ng",]
        
        if domain not in domain_list:
            raise forms.ValidationError("Please provide your official email address")
        return email
    
    # validate image format
    def clean_staff_image(self):
        data = self.cleaned_data['staff_image']
        filetype = data.split('.')[1]
        filetype_list = ["png", "jpg", "jpeg", "gif"]
        
        if filetype not in filetype_list:
            raise forms.ValidationError("Please upload a JPG, PNG or GIF file only")
        return data
    
    
    def form_valid(self, form):

        if form.is_valid:                
            cd = self.cleaned_data
            profile_image = cd.get['staff_image']
            
            if delete_image := cd.get['delete_image']:                
                profile_image = None
                #obj.staff_image = 'staffapp/static/img/default-male.jpg'
                form.save()
        return profile_image