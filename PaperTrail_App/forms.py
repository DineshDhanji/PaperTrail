from django.contrib.auth.forms import AuthenticationForm
from django import forms


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
