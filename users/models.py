from django.db import models

class Register(models.Model):
    username=models.CharField(max_length=100,unique=True)
    create_password=models.CharField(max_length=100)
    confirm_password=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)

# class Login(models.Model):
#     enter_username=models.CharField(max_length=100)
#     enter_password=models.CharField(max_length=100)
