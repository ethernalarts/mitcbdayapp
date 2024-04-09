import datetime
from dataclasses import fields
from enum import unique
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from django.urls import reverse  # To generate URLS by reversing URL patterns

# Create your models here.

default_pic = 'staffimages/default.png'
male_pic = 'staffimages/default-male.png'
female_pic = 'staffimages/default-female.png'


class staffDetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField('First Name', max_length=20, null=False)
    middle_name = models.CharField('Middle Name', max_length=20, null=True, blank=True)
    last_name = models.CharField('Last Name', max_length=20, null=False)
    phone_number = PhoneNumberField('Phone Number', null=False)
    official_email = models.EmailField('Official Email', max_length=254, null=False)

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
        ('Permanent Secretary', ('Permanent Secretary')),
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
        ('Human Resources', ('Human Resources')),
        ('Industry', ('Industry')),
        ('MSMEs', ('MSMEs')),
        ('Office of the Permanent Secretary', ('Office of the Permanent Secretary')),
        ('Office of the Honourable Commissioner', ('Office of the Honourable Commissioner')),
        ('Policy Formulation', ('Policy Formulation')),
        ('Planning, Research and Statistics', ('Planning, Research and Statistics')),
        ('Trade Promotions and Marketing', ('Trade Promotions and Marketing'))
    )

    department = models.CharField('Department', choices=DEPARTMENTS, max_length=100, null=False,
                                  default='Administration and Supply')
    level = models.IntegerField('Grade Level', null=False)
    step = models.IntegerField('Step', null=False)
    staff_image = models.ImageField("Profile Picture", upload_to='staffimages', default='staffimages/default.png')
    delete_image = models.BooleanField('Delete Profile Picture', default=0)

    @property
    def staff_image_default(self):
        return self._meta.get_field('staff_image').get_default()

    # profile picture
    # @property
    # def profile_picture(self):
    #     # Profile Picture
    #     if self.staff_image == default_pic:
    #         if self.gender == 1:
    #             self.staff_image = male_pic
    #         elif self.gender == 2:
    #             self.staff_image = female_pic

    #     # Update profile picture
    #     if (self.staff_image == male_pic) and (self.gender == 2):
    #         self.staff_image = female_pic
    #     if (self.staff_image == female_pic) and (self.gender == 1):
    #         self.staff_image = male_pic

    #     return self.staff_image

    # delete profile picture
    @property
    # def delete_profile_picture(self):
    #     if self.staff_image != [male_pic, female_pic, default_pic]:
    #         self.staff_image.delete()
    #         if self.gender == 1:
    #             self.staff_image = male_pic
    #             super().save()
    #         elif self.gender == 2:
    #             self.staff_image = female_pic
    #             super().save()
    #     return self.staff_image

    # get phone number
    @property
    def get_phone_number(self):
        if self.phone_number is None:
            self.phone_number = '0700 000 0000'
        return self.phone_number

    GENDER = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    gender = models.CharField(
        choices=GENDER,
        max_length=20,
        blank=False,
        default="Male",
    )

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

    date_of_birth = models.DateField(
        "Date of Birth", default=datetime.date.today, null=False, blank=False
    )

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
