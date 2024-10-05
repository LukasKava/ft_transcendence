from django import forms
from .models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'display_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user