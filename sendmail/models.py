
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date


# Create your models here.

class staffDetails(models.Model):
    """ Staff Details """
    
    first_name = models.CharField(max_length = 20)
    middle_name = models.CharField(max_length = 20, null = True, blank = True)
    last_name = models.CharField(max_length = 20)
    phone_number = PhoneNumberField(null = True, blank = True)
    email = models.EmailField(max_length = 254, help_text = 'Official Email(e.g. j.doe@edostate.gov.ng)')
    
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
        choices = MONTHS, 
        default = 1, 
        blank = False, 
        help_text = 'Birth month of staff')
    
    birth_day = models.IntegerField(blank = True, null = True)
    
    @property
    def bdaytoday(self):
        if (self.birth_month, self.birth_day) == (date.today().month, date.today().day):
            return True
        return False
    
    #birthdayToday = models.BooleanField(staffDetails().bdaytoday default=False)
    
    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
    