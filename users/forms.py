from django import forms
from .models import Register
from django.core.exceptions import ValidationError
import re

class registerForm(forms.ModelForm):
    class Meta:
        model=Register
        fields=['username','create_password','confirm_password']

    def clean_username(self):
        username=self.cleaned_data.get('username')
        if Register.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        return username
    
    def clean_create_password(self):
        password=self.cleaned_data.get('create_password')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("password must contain atleat one special character")
        return password 
    
    def clean(self):
        cleaned_data=super().clean()
        password=cleaned_data.get("create_password")
        confirm_password=cleaned_data.get("confirm_password")

        if password and confirm_password and password!=confirm_password:
            raise ValidationError("passwords do not match.")
        return cleaned_data

class LoginForm(forms.ModelForm):
    class Meta:
        model=Register
        fields=['username','create_password']

    def clean(self):
        cleaned_data=super().clean()
        username=cleaned_data.get("username")
        password=cleaned_data.get("create_password")
        user =Register.objects.filter(username=username,create_password=password).first()
        if not user:
            raise ValidationError("Invalid username or password.")
        return cleaned_data
