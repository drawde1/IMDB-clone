from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=36)
    password = forms.CharField(widget=forms.PasswordInput)


class SignupForm(forms.Form):
    username = forms.CharField(max_length=36)
    password = forms.CharField(widget=forms.PasswordInput)