
from email.policy import default
from enum import unique
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from django.urls import reverse  # To generate URLS by reversing URL patterns


# Create your models here.

class staffDetails(models.Model):
    """ Staff Details """
    
    first_name = models.CharField(verbose_name='First Name', max_length=20)
    
    middle_name = models.CharField(verbose_name='Middle Name', max_length=20, null=True, blank=True)
    
    last_name = models.CharField(verbose_name='Last Name', max_length=20)
    
    gender = models.CharField('Gender', max_length=10, default='Female')
    
    phone_number = PhoneNumberField('Phone Number', default='0800 000 0000')
    
    email = models.EmailField(verbose_name='Official Email', max_length = 254)   
     
    cadre = models.CharField(verbose_name='Cadre', max_length=50, null=True, blank=True)
    
    level = models.IntegerField('Level', default='1')
    
    step = models.IntegerField('Step', default='2', null=True, blank=True)
    
    staff_image = models.ImageField(
        verbose_name="Profile Picture",
        upload_to='staffimages', 
        default='staffimages/default.jpg', 
        null=True, 
        blank=True
    )
    
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
    
    birth_month = models.IntegerField(
        'Birth Month', 
        choices = MONTHS, 
        default = 1, 
        blank = False)
    
    birth_day = models.IntegerField(verbose_name='Birth Day', blank=True, null=True)
    
    
    class Meta:
        db_table = 'sendmail_staffdetails'
    
    
    def birth_month_verbose(self):
        return dict(staffDetails.MONTHS)[self.birth_month]
    
        
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
        """Returns the url to access a particular staff instance."""
        return reverse('updatestaff', args=[str(self.id)])
    
    
    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
    