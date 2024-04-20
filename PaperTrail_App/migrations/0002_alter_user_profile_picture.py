# Generated by Django 5.0.4 on 2024-04-20 16:52

import PaperTrail_App.custom_validator
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PaperTrail_App', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(default='profile_pics/default_pp.jpg', upload_to='profile_pics/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']), PaperTrail_App.custom_validator.validate_profilePicture_size]),
        ),
    ]