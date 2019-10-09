from django.db import models
from core.models import Child, App
from django.utils.timezone import localtime

class Transaction(models.Model):
    PAYMENT_METHODS = (

        ('online', 'Online'),
        ('offline', 'Offline')

    )



    transactID = models.CharField(max_length=32, primary_key=True)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paymentTime = models.DateTimeField(default=localtime().now())
    terminal = models.CharField(max_length=32)
    mfo = models.CharField(max_length=5)
    paymentMethod = models.CharField(choices=PAYMENT_METHODS, default=PAYMENT_METHODS[0], max_length=12)
    cheque = models.FileField(upload_to='cheques', blank=True)
    appType = models.ForeignKey(App, on_delete=models.CASCADE)

    def __str__(self):
        return '{fN} {s}'  .format(fN=self.child, s=self.amount)
