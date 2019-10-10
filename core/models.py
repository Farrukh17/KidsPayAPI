from django.db import models
from django.utils.timezone import now


class Child(models.Model):
    id = models.CharField(primary_key=True, max_length=7)
    firstName = models.CharField(max_length=30, verbose_name='Имя')
    middleName = models.CharField(max_length=30, blank=True)
    lastName = models.CharField(max_length=30, verbose_name='Фамилия')
    enteredDate = models.DateField(default=now(), verbose_name='Дата вступления')
    father = models.CharField(max_length=100, blank=True, verbose_name='Отец')
    contactFather = models.CharField(max_length=12, blank=True, verbose_name='Контактный телефон отца')
    mother = models.CharField(max_length=100, blank=True, verbose_name='Мать')
    contactMother = models.CharField(max_length=12, blank=True, verbose_name='Контактный телефон матери')
    monthlyFee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Ежемесячный взнос')
    agreementNumber = models.CharField(max_length=20, default='Номер и дата договора')
    birthCertificateNumber = models.CharField(max_length=20, default='', verbose_name='Номер свидетельства о рождении')
    school = models.ForeignKey('School', on_delete=models.CASCADE, null=True, verbose_name='Детский садик')
    group = models.ForeignKey('Group', on_delete=models.CASCADE, null=True, verbose_name='Группа')
    debt = models.DecimalField(max_digits=12, default=0.00, decimal_places=2, verbose_name='Задолженность')

    class Meta:
        verbose_name = 'Воспитанник'
        verbose_name_plural = 'Воспитанники'

    def __str__(self):
        return '{fN} {mN} {lN}'.format(fN=self.firstName, mN=self.middleName, lN=self.lastName)


class School(models.Model):
    STATUSES = (
        ('active', "Active"),
        ('deactive', "Deactive"),
        ('stopped', "Stopped")
    )
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Детский садик')
    directorName = models.CharField(max_length=100, verbose_name='Ф.И.О. директора')
    contactDirector = models.CharField(max_length=12, verbose_name='Контактный номер директора')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    status = models.CharField(choices=STATUSES, default=STATUSES[0], max_length=12, verbose_name='Статус')
    agreementDocNumber = models.CharField(max_length=30, blank=True, verbose_name='Номер договора')

    class Meta:
        verbose_name = 'Детский садик'
        verbose_name_plural = 'Детский садики'

    def __str__(self):
        return '{fN}'.format(fN=self.name)


class Group(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, verbose_name='Название группы')
    fee = models.DecimalField(max_digits=12, decimal_places=2,default=0.00, verbose_name='Ежемесячный взнос')
    maxNumberOfChild = models.SmallIntegerField(blank=True, default=10, verbose_name='Максимальное количество детей')
    subGroup = models.ForeignKey('Group', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Номер группы')
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name='Детский садик')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


    def __str__(self):
        return '{fN}'.format(fN=self.name)


class App(models.Model):

    STATUSES = (
        ('active', "Active"),
        ('inactive', "Inactive"),
        ('stopped', "Stopped")
    )

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=24, verbose_name='Название приложения')
    token = models.CharField(max_length=32, verbose_name='Токен')
    status = models.CharField(choices=STATUSES, default=STATUSES[0], max_length=12, verbose_name='Статус')

    class Meta:
        verbose_name = 'Приложение'
        verbose_name_plural = 'Приложения'

    def __str__(self):
        return '{fN}'.format(fN=self.name)