
import os
import datetime
from email.policy import default
from enum import unique
from django.db import models
from numpy import True_, require
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from django.urls import reverse  # To generate URLS by reversing URL patterns


# Create your models here.

class staffDetails(models.Model):
    
    first_name = models.CharField('First Name', max_length=20, null=False)    
    middle_name = models.CharField('Middle Name', max_length=20, null=True, blank=True)    
    last_name = models.CharField('Last Name', max_length=20, null=False)    
    phone_number = PhoneNumberField(('Phone Number'), default='08012345678')    
    email = models.EmailField('Official Email', max_length = 254, null=False)        
    cadre = models.CharField(("Cadre"), max_length=50, null=False, default='Admin Officer')    
    first_appointment = models.DateField(("Date of First Appointment"), default=datetime.date.today, null=False, blank=False)    
    department = models.CharField('Department', max_length=100, null=False, default='Adminstration')    
    level = models.IntegerField('Grade Level', null=False)    
    step = models.IntegerField('Step', null=False)  
    
    def default_profile_pic(self):
        if self.gender_text=='Female':
            default = 'static/img/default-female.jpg'
        elif self.gender_text=='Male':
            default = 'static/img/default-male.jpg'
        return default
    
    staff_image = models.ImageField(("Profile Picture"), upload_to='staffimages', default='staffimages/default.jpg')
    delete_image = models.BooleanField('Delete Profile Picture', default=0)    
    
    # def deleteProfilePicture(self,*args,**kwargs):
    #     if os.path.isfile(self.staff_image.path):
    #         os.remove(self.staff_image.path)

    #     super(staffDetails, self).delete(*args,**kwargs)
    
    def delete(self, using=None, keep_parents=False):
        self.staff_image.storage.delete(self.staff_image.first_name)
        super().delete()
        
    GENDER = (
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Prefer not to say')
    )
        
    gender = models.IntegerField('Gender', choices=GENDER, default=2)    
    
    def gender_text(self):
        return dict(staffDetails.GENDER)[self.gender]
    
    MONTHS = (
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December')
    )
    
    birth_month = models.IntegerField('Birth Month', choices=MONTHS, default=1)    
    birth_day = models.IntegerField('Birth Day', null=False)    
    
    def birth_month_verbose(self):
        return dict(staffDetails.MONTHS)[self.birth_month]    
    
    class Meta:
        db_table = 'birthday_staffdetails'    
        
    def phone_number_default(self):
        return staffDetails._meta.get_field('phone_number').get_default()    
        
    @property
    def BIRTHDAY_TODAY(self):
        if (self.birth_month, self.birth_day) == (date.today().month, date.today().day):
            return True
        return False    
    
    # Staff Details Reverse URL
    def get_absolute_url(self):
        """Returns the url to access a particular staff instance."""
        return reverse('staffdetails', args=[str(self.id)])    
    
    # Update Staff Reverse URL
    def get_absolute_url_update_staff(self):
        """Returns the url to update a particular staff instance."""
        return reverse('updatestaff', args=[str(self.id)])    
    
    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
    