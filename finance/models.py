import datetime
from django.db import models
from core.models import Child, App, School
from django.utils.timezone import localtime


def get_cheque_upload_folder(instance, filename):
    dt = datetime.datetime.today()
    return 'cheques/{school}/{year}-{month}/{filename}'.format(school=instance.school.name, year=dt.year,
                                                               month=dt.month, filename=filename)


class Transaction(models.Model):
    PAYMENT_METHODS = (
        ('online', 'Online'),
        ('offline', 'Offline')
    )
    transactID = models.CharField(max_length=32, primary_key=True, verbose_name='Номер транзакции')
    child = models.ForeignKey(Child, related_name='transactions', on_delete=models.CASCADE, verbose_name='Ф.И.О. воспитанника')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма оплаты')
    paymentTime = models.DateTimeField(default=localtime().now(), verbose_name='Время оплаты')
    terminal = models.CharField(max_length=32, verbose_name='Терминал', blank=True, null=True)
    mfo = models.CharField(max_length=5, verbose_name='МФО банка')
    paymentMethod = models.CharField(choices=PAYMENT_METHODS, default=PAYMENT_METHODS[1][0], max_length=12, verbose_name='Метод оплаты', null=True)
    cheque = models.FileField(upload_to=get_cheque_upload_folder, null=True, verbose_name='Чек')
    appType = models.ForeignKey(App, on_delete=models.CASCADE, verbose_name='Название приложение', null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='transactions', null=True)

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return '{child} - {amount} UZS - {month}'.format(child=self.child, amount=self.amount, month=self.paymentTime.strftime('%Y.%m.%d'))

    def clean(self):
        self.paymentMethod = self.PAYMENT_METHODS[1][0]
        self.child.balance += self.amount
        self.child.save()
