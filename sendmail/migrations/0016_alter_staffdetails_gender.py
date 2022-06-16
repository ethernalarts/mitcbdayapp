# Generated by Django 4.0.5 on 2022-06-14 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sendmail', '0015_alter_staffdetails_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffdetails',
            name='gender',
            field=models.IntegerField(choices=[(1, 'Male'), (2, 'Female'), (3, 'Prefer not to say')], default=2, verbose_name='Gender'),
        ),
    ]