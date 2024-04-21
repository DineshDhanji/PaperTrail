from django.contrib.auth.forms import AuthenticationForm


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
