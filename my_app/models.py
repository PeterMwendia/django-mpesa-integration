from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15)

class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    merchant_request_id = models.CharField(max_length=255)
    checkout_request_id = models.CharField(max_length=255)
    result_code = models.IntegerField()
    result_desc = models.CharField(max_length=255)
    amount = models.IntegerField()
    mpesa_receipt_number = models.CharField(max_length=255)
    transaction_date = models.CharField(max_length=255)
    
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('TP', 'Token Purchase'),
        # Add other transaction types here
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField()
    transaction_type = models.CharField(max_length=2, choices=TRANSACTION_TYPES)
    result_code = models.IntegerField()
    result_desc = models.CharField(max_length=255)