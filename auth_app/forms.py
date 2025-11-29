from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        label="First Name"
    )

    last_name = forms.CharField(
        required=True,
        label="Last Name"
    )

    email = forms.EmailField(
        required=True,
        label="Email Address",
        help_text="Required. Must be unique."
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text="Minimum 8 characters with strong password rules."
    )

    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        ]  # password_confirm is NOT part of User model

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if not password:
            raise ValidationError("Password is required.")

        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationError(e.messages)

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        """
        Save user + hash password + save name + save email.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
        return user
