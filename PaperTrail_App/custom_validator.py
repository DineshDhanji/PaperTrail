from django.core.exceptions import ValidationError


def validate_profilePicture_size(value):
    limit = 7 * 1024 * 1024  # 7 MB in bytes
    if value.size > limit:
        raise ValidationError("File size cannot exceed 7 MB.")
