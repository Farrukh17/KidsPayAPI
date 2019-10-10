from django.db import models
from core.models import Child, App
from django.utils.timezone import localtime


class Transaction(models.Model):
    PAYMENT_METHODS = (

        ('online', 'Online'),
        ('offline', 'Offline')

    )
    transactID = models.CharField(max_length=32, primary_key=True, verbose_name='Номер транзакции')
    child = models.ForeignKey(Child, on_delete=models.CASCADE, verbose_name='Ф.И.О. воспитанника')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма оплаты')
    paymentTime = models.DateTimeField(default=localtime().now(), verbose_name='Время оплаты')
    terminal = models.CharField(max_length=32, verbose_name='Терминал')
    mfo = models.CharField(max_length=5, verbose_name='МФО банка')
    paymentMethod = models.CharField(choices=PAYMENT_METHODS, default=PAYMENT_METHODS[0], max_length=12, verbose_name='Метод оплаты')
    cheque = models.FileField(upload_to='cheques', blank=True, verbose_name='Чек')
    appType = models.ForeignKey(App, on_delete=models.CASCADE, verbose_name='Название приложение')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return '{fN} {s}'  .format(fN=self.child, s=self.amount)
