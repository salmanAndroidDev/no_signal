from django import forms
from django.contrib.auth import get_user_model


class UserRegistrationForm(forms.ModelForm):
    """
        Custom form to handle user registration
    """
    class Meta:
        model = get_user_model()

    def save(self, commit=True):
        pass