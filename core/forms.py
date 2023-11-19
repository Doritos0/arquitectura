from django import forms

class LoginForm(forms.Form):
    user = forms.CharField(max_length=20, min_length=4, required=True)
    password = forms.CharField(max_length=20, min_length=4, required=True)
