
from dataclasses import fields
import datetime
from enum import unique
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from django.urls import reverse  # To generate URLS by reversing URL patterns


# Create your models here.


class staffDetails(models.Model):
    
    first_name = models.CharField('First Name', max_length=20, null=False)    
    middle_name = models.CharField('Middle Name', max_length=20, null=True, blank=True)    
    last_name = models.CharField('Last Name', max_length=20, null=False)    
    phone_number = PhoneNumberField('Phone Number', null=False)        
    email = models.EmailField('Official Email', max_length = 254, null=False)
    
    CADRE = (
        ('Administrative', ('Administrative')),
        ('Account Officer', ('Account Officer')),
        ('Executive', ('Executive')),
        ('Chief Secretary Assistant', ('Chief Secretary Assistant')),
        ('Commercial Officer', ('Commercial Officer')),
        ('Confidential Secretary', ('Confidential Secretary')),
        ('Cooperative Officer', ('Cooperative Officer')),
        ('Driver/Mechanic', ('Driver/Mechanic')),
        ('Industrial Promotion Officer', ('Industrial Promotion Officer')),
        ('Messenger', ('Messenger')),
        ('Procurement', ('Procurement')),
        ('Program Analyst', ('Program Analyst')),
        ('Statistician', ('Statistician')),
        ('Stores Officer', ('Stores Officer')),
        ('Trade Officer', ('Trade Officer')),
        ('Watchman', ('Watchman'))
    )
    
    cadre = models.CharField(('Cadre'), choices=CADRE, max_length=100, null=False, default='Administrative')   
    first_appointment = models.DateField(("Date of First Appointment"), default=datetime.date.today, null=False)    
    
    DEPARTMENTS = (
        ('Accounts', ('Accounts')),
        ('Business Premises', ('Business Premises')),
        ('Cooperatives', ('Cooperatives')),
        ('Human Resource', ('Human Resource')),
        ('Industry', ('Industry')),
        ('MSMEs', ('MSMEs')),
        ('Office of the Permanent Secretary', ('Office of the Permanent Secretary')),
        ('Office of the Honourable Commissioner', ('Office of the Honourable Commissioner')),
        ('Policy Formulation', ('Policy Formulation')),
        ('Planning, Research and Statistics', ('Planning, Research and Statistics')),
        ('Trade Promotions and Marketing', ('Trade Promotions and Marketing'))
    )        
        
    department = models.CharField('Department', choices=DEPARTMENTS, max_length=100, null=False, default='Administration and Supply')    
    level = models.IntegerField('Grade Level', null=False)    
    step = models.IntegerField('Step', null=False)     
    staff_image = models.ImageField("Profile Picture", upload_to='staffimages', default='staffimages/default.png')
    delete_image = models.BooleanField('Delete Profile Picture', default=0)    
    
    # profile picture
    @property
    def profile_picture(self):   
        # Profile Picture
        if self.staff_image == 'staffimages/default.png':
            if self.gender == 1:
                self.staff_image = 'staffimages/default-male.png'
            elif self.gender == 2:
                self.staff_image = 'staffimages/default-female.png'

        # Update profile picture  
        if (self.staff_image == 'staffimages/default-male.png') and (self.gender == 2):
            self.staff_image = 'staffimages/default-female.png'
        if (self.staff_image == 'staffimages/default-female.png') and (self.gender == 1):
            self.staff_image = 'staffimages/default-male.png'
        return self.staff_image 
    
    # delete profile picture
    @property    
    def delete_profile_picture(self):
        if self.delete_image:            
            self.staff_image.storage.delete(self.staff_image.first_name)
            super().delete()
    
    # get phone number
    @property
    def get_phone_number(self):
        if self.phone_number is None:
            self.phone_number = '0700 000 0000'
        return self.phone_number
        
    GENDER = ((1, 'Male'), (2, 'Female'))
        
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
        return (self.birth_month, self.birth_day) == (date.today().month, date.today().day)    
    
    # Staff Details Reverse URL
    def get_absolute_url(self):
        """Returns the url to access a particular staff instance."""
        return reverse('staffdetails', args=[str(self.id)])    
    
    # Update Staff Reverse URL
    def get_absolute_url_update_staff(self):
        """Returns the url to update a particular staff instance."""
        return reverse('updatestaff', kwargs={'pk': self.id})  
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    