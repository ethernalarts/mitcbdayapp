# Generated by Django 4.0.5 on 2022-06-13 00:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sendmail', '0013_remove_staffdetails_position_staffdetails_cadre_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staffdetails',
            old_name='staffimage',
            new_name='staff_image',
        ),
    ]