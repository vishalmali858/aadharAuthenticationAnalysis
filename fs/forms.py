from django import forms
from django.contrib.auth.models import User
from .models import Us

class RegisterForm(forms.ModelForm):

    class Meta:
        model = Us
        fields = ['em', 'cn', 'rl','ic']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Us
        fields = ['username', 'password']

class ForgetForm(forms.ModelForm):

    class Meta:
        model = Us
        fields = ['username']

class OTPForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Us
        fields = ['otp']
