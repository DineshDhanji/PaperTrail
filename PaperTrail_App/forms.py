from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from .models import User


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        # Add classes and placeholders to the fields
        self.fields["username"].widget.attrs.update(
            {
                "class": "input-field rounded col-sm-12 col-md-10 px-2",
                "placeholder": "Enter your username",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": "input-field rounded col-sm-12 col-md-10 px-2",
                "placeholder": "Enter your password",
            }
        )


class UserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        # Add classes and placeholders to the fields
        self.fields["username"].widget.attrs.update(
            {
                "class": "input-field rounded col-sm-12 col-md-10 px-2",
                "placeholder": "Enter your username",
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "class": "input-field rounded col-sm-12 col-md-10 px-2",
                "placeholder": "Enter your password",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "input-field rounded col-sm-12 col-md-10 px-2",
                "placeholder": "Retype your password",
            }
        )

    class Meta:
        model = User  
        fields = ["username", "password1", "password2"]  


class DocumentForm(forms.Form):
    ALLOWED_EXTENSIONS = ["docx", "pdf", "png", "jpg", "jpeg"]

    document = forms.FileField(
        label="Click here to upload your doc!",
        help_text="Allowed file types: docx, pdf, png, jpg, jpeg",
        widget=forms.ClearableFileInput(
            attrs={"accept": "image/*,.docx,.pdf"}
        ),  # Specify accepted file types
        required=True,  # Ensure the field is marked as required
    )

    def clean_document(self):
        document = self.cleaned_data["document"]
        if document:
            file_name = document.name
            file_extension = file_name.split(".")[-1].lower()
            if file_extension not in self.ALLOWED_EXTENSIONS:
                raise forms.ValidationError(
                    f'The file "{file_name}" has an unsupported file type.'
                )
        return document
