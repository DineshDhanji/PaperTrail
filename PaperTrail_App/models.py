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


class Document(models.Model):
    DOC_CHOICES = (
        ("pdf", "PDF"),
        ("docx", "DOCX"),
        ("img", "Image"),
    )

    doc = models.FileField(upload_to="documents/")
    doc_name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="docs")
    doc_type = models.CharField(max_length=4, choices=DOC_CHOICES)

    def __str__(self):
        return self.doc_name

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
