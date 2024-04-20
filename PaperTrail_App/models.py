from django.db import models
from django.contrib.auth.models import AbstractUser

from .custom_validator import validate_profilePicture_size
from django.core.validators import FileExtensionValidator


class User(AbstractUser):
    # It already have first_name, last_name, email, password
    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        null=False,
        default="profile_pics/default_pp.jpg",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png"]
            ),  # Restrict allowed file extensions
            validate_profilePicture_size,  # Set a maximum file size limit (7 MB in this example)
        ],
    )
    