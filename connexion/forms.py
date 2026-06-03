from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile , Company
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("password1", "password2")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['company']
        fields = ['phone', 'address']


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name']


User = get_user_model()

class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']