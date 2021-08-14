from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """
        Custom form to handle user registration
    """

    class Meta:
        model = get_user_model()
        fields = ('name', 'email')
