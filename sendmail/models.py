
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from django.urls import reverse  # To generate URLS by reversing URL patterns


# Create your models here.

class staffDetails(models.Model):
    """ Staff Details """
    
    first_name = models.CharField(verbose_name='First Name', max_length = 20)
    middle_name = models.CharField(verbose_name='Middle Name', max_length = 20, null = True, blank = True)
    last_name = models.CharField(verbose_name='Last Name', max_length = 20)
    phone_number = PhoneNumberField(verbose_name='Phone Number', null = True, blank = True)
    email = models.EmailField(verbose_name='Official Email', max_length = 254, help_text = 'Official Email(e.g. j.doe@edostate.gov.ng)')
    
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
    
    birth_day = models.IntegerField(verbose_name='Birth Day', blank = True, null = True)
    
    @property
    def BIRTHDAY_TODAY(self):
        if (self.birth_month, self.birth_day) == (date.today().month, date.today().day):
            return True
        return False
    
    def get_absolute_url(self):
        """Returns the url to access a particular staff instance."""
        return reverse('staffdetails', args=[str(self.id)])
    
    
    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
    