# Generated by Django 4.0.6 on 2022-07-12 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sendmail', '0028_alter_staffdetails_staff_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffdetails',
            name='staff_image',
            field=models.ImageField(default='staffimages/default-female.jpg', upload_to='staffimages', verbose_name='Profile Picture'),
        ),
    ]