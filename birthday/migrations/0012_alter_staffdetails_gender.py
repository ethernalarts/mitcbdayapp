# Generated by Django 4.0.6 on 2022-07-23 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birthday', '0011_alter_staffdetails_staff_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffdetails',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=30, null=True, verbose_name='Gender'),
        ),
    ]
