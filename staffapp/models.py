import datetime
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from django.urls import reverse

# Create your models here.

default_pic = "staffimages/default.png"
male_pic = "staffimages/default-male.png"
female_pic = "staffimages/default-female.png"


class staffDetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField("First Name", max_length=20, null=False)
    middle_name = models.CharField("Middle Name", max_length=20, null=True, blank=True, default="")
    last_name = models.CharField("Last Name", max_length=20, null=False)
    phone_number = PhoneNumberField("Phone Number", null=False)
    official_email = models.EmailField("Official Email", max_length=254, null=False)

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

    CADRE = (
        ("Administrative", "Administrative"),
        ("Assistant Director", "Assistant Director"),
        ("Account Officer", "Account Officer"),
        ("Executive", "Executive"),
        ("Chief Secretary Assistant", "Chief Secretary Assistant"),
        ("Commercial Officer", "Commercial Officer"),
        ("Confidential Secretary", "Confidential Secretary"),
        ("Cooperative Officer", "Cooperative Officer"),
        ("Director", "Director"),
        ("Driver/Mechanic", "Driver/Mechanic"),
        ("Industrial Promotion Officer", "Industrial Promotion Officer"),
        ("Messenger", "Messenger"),
        ("Permanent Secretary", "Permanent Secretary"),
        ("Procurement", "Procurement"),
        ("Program Analyst", "Program Analyst"),
        ("Statistician", "Statistician"),
        ("Stores Officer", "Stores Officer"),
        ("Trade Officer", "Trade Officer"),
        ("Watchman", "Watchman"),
    )

    DEPARTMENTS = (
        ("Accounts", "Accounts"),
        ("Business Premises", "Business Premises"),
        ("Cooperatives", "Cooperatives"),
        ("Human Resources", "Human Resources"),
        ("Industry", "Industry"),
        ("MSMEs", "MSMEs"),
        ("Office of the Permanent Secretary", "Office of the Permanent Secretary"),
        (
            "Office of the Honourable Commissioner",
            "Office of the Honourable Commissioner",
        ),
        ("Policy Formulation", "Policy Formulation"),
        ("Planning, Research and Statistics", "Planning, Research and Statistics"),
        ("Trade Promotions and Marketing", "Trade Promotions and Marketing"),
    )

    GRADE_LEVEL = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (12, 12),
        (13, 13),
        (14, 14),
        (15, 15),
        (16, 16),
        (17, 17),
    )

    STEP = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    )

    cadre = models.CharField(
        "Cadre", choices=CADRE, max_length=100, null=False, default="Administrative"
    )
    first_appointment = models.DateField(
        "Date of First Appointment", default=datetime.date.today, null=False, blank=True
    )
    date_of_birth = models.DateField(
        "Date of Birth", default=datetime.date.today, null=False, blank=True
    )

    department = models.CharField(
        "Department",
        choices=DEPARTMENTS,
        max_length=100,
        null=False,
        default="Administration and Supply",
    )
    grade_level = models.IntegerField("Grade Level", default=1, choices=GRADE_LEVEL, null=False)
    step = models.IntegerField("Step", default=1, choices=STEP, null=False)
    staff_image = models.ImageField(
        "Profile Picture", upload_to="staffimages", default="staffimages/default.png"
    )
    delete_image = models.BooleanField("Delete Profile Picture", default=0)

    @property
    def staff_image_default(self):
        return self._meta.get_field("staff_image").get_default()

    # get phone number
    @property
    def get_phone_number(self):
        if self.phone_number is None:
            self.phone_number = "0700 000 0000"
        return self.phone_number

    def birth_month_verbose(self):
        return dict(staffDetails.MONTHS)[self.birth_month]

    @property
    def BIRTHDAY_TODAY(self):
        return (self.birth_month, self.birth_day) == (
            date.today().month,
            date.today().day,
        )

        # Staff Details Reverse URL

    def get_absolute_url(self):
        return reverse("staffdetails", kwargs={"pk": self.id})

    def get_absolute_url_update_staff(self):
        """Returns the url to update a particular staff instance."""
        return reverse("updatestaff", kwargs={"pk": self.id})

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "birthday_staffdetails"
