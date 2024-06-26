# Generated by Django 5.0.4 on 2024-04-15 11:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staffapp", "0004_alter_staffdetails_step"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staffdetails",
            name="date_of_birth",
            field=models.DateField(
                blank=True, default=datetime.date.today, verbose_name="Date of Birth"
            ),
        ),
        migrations.AlterField(
            model_name="staffdetails",
            name="first_appointment",
            field=models.DateField(
                blank=True,
                default=datetime.date.today,
                verbose_name="Date of First Appointment",
            ),
        ),
    ]
