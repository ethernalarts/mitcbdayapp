
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from birthday.models import staffDetails


# Add Staff form
class staffDetailsCreateForm(forms.ModelForm):    
    
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
            raise ValidationError("Error! Please enter your official email address")
        return data   
        
        
# Update Staff form
class staffDetailsUpdateForm(forms.ModelForm):      
    staff_image = forms.ImageField(label='Change Profile Picture', widget=forms.FileInput, required=False) 
    
    class Meta: 
        model = staffDetails 
        fields = [
            'first_name', 'middle_name', 'last_name', 'gender', 'phone_number', 'email', 
            'cadre', 'first_appointment', 'department', 'level', 'step', 'staff_image', 
            'birth_month', 'birth_day', 'delete_image'
        ]   
    
    # validate email domain name
    def clean_email(self):
        data = self.cleaned_data['email']
        domain = data.split('@')[1]
        domain_list = ["edostate.gov.ng",]
        
        if domain not in domain_list:
            raise forms.ValidationError("Please enter an Email Address with a valid domain")
        return data
    
    # profile picture
    # def clean_staff_image(self):
    #     delete_image = self.cleaned_data['delete_image']
    #     gender = self.cleaned_data['gender']
        
    #     if image == '':
    #         if gender == 2:
    #             image = 'staffimages/default-female.png'
    #         elif gender == 1:
    #             image = 'staffimages/default-male.png'
    #     return image
    
    def form_valid(self, form):                
        cd = self.cleaned_data
        profile_image = cd.get['staff_image']

        if delete_image := cd.get['delete_image']:
            if form.is_valid:                
                profile_image = None
                #obj.staff_image = 'staffapp/static/img/default-male.jpg'
                form.save()
        return profile_image