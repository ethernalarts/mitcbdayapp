# Generated by Django 5.0.4 on 2024-04-09 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staffapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staffdetails",
            name="gender",
            field=models.CharField(
                choices=[("Male", "Male"), ("Female", "Female")],
                default="Male",
                max_length=20,
            ),
        ),
    ]
