# Generated by Django 4.0.6 on 2022-07-15 20:18

import datetime
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='staffDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20, verbose_name='First Name')),
                ('middle_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Middle Name')),
                ('last_name', models.CharField(max_length=20, verbose_name='Last Name')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(default='08012345678', max_length=128, region=None, verbose_name='Phone Number')),
                ('email', models.EmailField(max_length=254, verbose_name='Official Email')),
                ('cadre', models.CharField(default='Admin Officer', max_length=50, verbose_name='Cadre')),
                ('first_appointment', models.DateField(default=datetime.date.today, verbose_name='Date of First Appointment')),
                ('department', models.CharField(default='Adminstration', max_length=100, verbose_name='Department')),
                ('level', models.IntegerField(verbose_name='Grade Level')),
                ('step', models.IntegerField(verbose_name='Step')),
                ('staff_image', models.ImageField(default='staffimages/default.jpg', upload_to='staffimages', verbose_name='Profile Picture')),
                ('gender', models.IntegerField(choices=[(1, 'Male'), (2, 'Female'), (3, 'Prefer not to say')], default=2, verbose_name='Gender')),
                ('birth_month', models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=1, verbose_name='Birth Month')),
                ('birth_day', models.IntegerField(verbose_name='Birth Day')),
            ],
            options={
                'db_table': 'birthday_staffdetails',
            },
        ),
    ]
