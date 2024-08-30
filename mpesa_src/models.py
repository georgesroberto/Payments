from django.db import models

# Create your models here.
class MpesaTransaction(models.Model):
    merchant_request_id = models.CharField(max_length=255)
    checkout_request_id = models.CharField(max_length=255)
    result_code = models.IntegerField(null=True, blank=True)
    result_desc = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    transaction_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
