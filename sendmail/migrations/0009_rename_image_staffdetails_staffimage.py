# Generated by Django 4.0.5 on 2022-06-08 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sendmail', '0008_auto_20220607_2102'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staffdetails',
            old_name='image',
            new_name='staffimage',
        ),
    ]