# Generated by Django 4.0.6 on 2022-07-18 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birthday', '0005_rename_remove_image_staffdetails_delete_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffdetails',
            name='delete_image',
            field=models.BooleanField(default=0, verbose_name='Delete Profile Picture'),
        ),
    ]
