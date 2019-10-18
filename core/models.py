from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist


class Child(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    firstName = models.CharField(max_length=30, verbose_name='Имя')
    middleName = models.CharField(max_length=30, blank=True)
    lastName = models.CharField(max_length=30, verbose_name='Фамилия')
    group = models.ForeignKey('Group', related_name='children', on_delete=models.CASCADE, null=True, verbose_name='Группа')
    enteredDate = models.DateField(default=now(), verbose_name='Дата вступления')
    father = models.CharField(max_length=100, blank=True, verbose_name='Отец')
    contactFather = models.CharField(max_length=12, blank=True, verbose_name='Контактный телефон отца')
    mother = models.CharField(max_length=100, blank=True, verbose_name='Мать')
    contactMother = models.CharField(max_length=12, blank=True, verbose_name='Контактный телефон матери')
    monthlyFee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Ежемесячный взнос')
    agreementNumber = models.CharField(max_length=20, verbose_name='Номер и дата договора')
    birthCertificateNumber = models.CharField(max_length=20, default='', verbose_name='Номер свидетельства о рождении')
    school = models.ForeignKey('School', on_delete=models.CASCADE, null=True, verbose_name='Детский садик')
    debt = models.DecimalField(max_digits=12, default=0.00, decimal_places=2, verbose_name='Задолженность')
    child_number = models.CharField(max_length=4, blank=True, null=True, verbose_name='Воспитанник ID')

    class Meta:
        verbose_name = 'Воспитанник'
        verbose_name_plural = 'Воспитанники'

    def __str__(self):
        return '{fN} {mN} {lN}'.format(fN=self.firstName, mN=self.middleName, lN=self.lastName)

    def clean(self):
        try:
            if not self.id:
                n = str(int(Child.objects.filter(id__startswith=self.school.id+':').latest('id').id.split(':')[1]) + 1)
                self.id = self.school.id + ':' + n.zfill(4)
                self.child_number = n
        except ObjectDoesNotExist:
            self.id = self.school.id + ':0001'
            self.child_number = '1'


class School(models.Model):
    STATUSES = (
        ('active', "Active"),
        ('inactive', "Inactive"),
        ('stopped', "Stopped")
    )
    id = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Детский садик')
    directorName = models.CharField(max_length=100, verbose_name='Ф.И.О. директора')
    contactDirector = models.CharField(max_length=12, verbose_name='Контактный номер директора', help_text='Например: 998901234567')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    status = models.CharField(choices=STATUSES, default=STATUSES[0][0], max_length=12, verbose_name='Статус')
    agreementDocNumber = models.CharField(max_length=30, blank=True, verbose_name='Номер договора')

    class Meta:
        verbose_name = 'Детский садик'
        verbose_name_plural = 'Детские садики'

    def __str__(self):
        return '{name}'.format(name=self.name)

    def clean(self):
        try:
            if not self.id:
                n = str(int(School.objects.latest('id').id) + 1)
                self.id = n.zfill(5)
        except ObjectDoesNotExist:
            self.id = '00001'


class Group(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, verbose_name='Название группы')
    fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Ежемесячный взнос')
    maxNumberOfChild = models.SmallIntegerField(blank=True, default=20, verbose_name='Максимальное количество детей')
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name='Детский садик')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return '{name}'.format(name=self.name)

    def clean(self):
        if not self.id:
            self.id = Group.objects.latest('id').id + 1


class App(models.Model):
    STATUSES = (
        ('active', "Active"),
        ('inactive', "Inactive"),
        ('stopped', "Stopped")
    )

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=24, verbose_name='Название приложения')
    token = models.CharField(max_length=32, verbose_name='Токен')
    status = models.CharField(choices=STATUSES, default=STATUSES[0][0], max_length=12, verbose_name='Статус')

    class Meta:
        verbose_name = 'Приложение'
        verbose_name_plural = 'Приложения'

    def __str__(self):
        return '{name}'.format(name=self.name)

    def clean(self):
        if not self.id:
            self.id = App.objects.latest('id').id + 1


class Admin(AbstractUser):
    ADMIN_TYPES = (
        ('superuser', 'SuperUser'),
        ('admin', 'Admin'),
        ('director', 'Director'),
        ('accountant', 'Accountant')
    )
    type = models.CharField(choices=ADMIN_TYPES, default=ADMIN_TYPES[1][0], max_length=12, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
