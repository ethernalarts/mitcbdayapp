# Generated by Django 4.0.6 on 2022-07-17 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birthday', '0003_staffdetails_remove_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffdetails',
            name='remove_image',
            field=models.BooleanField(default=0, verbose_name='Remove Profile Picture'),
        ),
    ]
