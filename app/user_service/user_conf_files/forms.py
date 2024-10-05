from django import forms
from .models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'display_name', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        password = forms.CharField(widget=forms.PasswordInput)
        if commit:
            user.save()
        return user