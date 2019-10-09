from django.db import models
from django.utils.timezone import now


class Child(models.Model):
    id = models.CharField(primary_key=True, max_length=7)
    firstName = models.CharField(max_length=30, verbose_name='Имя')
    middleName = models.CharField(max_length=30, blank=True)
    lastName = models.CharField(max_length=30, verbose_name='Фамилия')
    enteredDate = models.DateField(default=now())
    father = models.CharField(max_length=100, blank=True)
    contactFather = models.CharField(max_length=12, blank=True)
    mother = models.CharField(max_length=100, blank=True)
    contactMother = models.CharField(max_length=12, blank=True)
    monthlyFee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    agreementNumber = models.CharField(max_length=20, default='')
    birthCertificateNumber = models.CharField(max_length=20, default='')
    school = models.ForeignKey('School', on_delete=models.CASCADE, null=True)
    debt = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)

    def __str__(self):
        return '{fN} {mN} {lN}'.format(fN=self.firstName, mN=self.middleName, lN=self.lastName)


class School(models.Model):
    STATUSES = (
        ('active', "Active"),
        ('deactive', "Deactive"),
        ('stopped', "Stopped")
    )

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    directorName = models.CharField(max_length=100)
    contactDirector = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    status = models.CharField(choices=STATUSES, default=STATUSES[0], max_length=12)
    agreementDocNumber = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return '{fN}'.format(fN=self.name)


class Group(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    fee = models.DecimalField(max_digits=12, decimal_places=2,default=0.00)
    maxNumberOfChild = models.SmallIntegerField(blank=True, default=10)
    subGroup = models.ForeignKey('Group', on_delete=models.CASCADE, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    def __str__(self):
        return '{fN}'.format(fN=self.name)


class App(models.Model):

    STATUSES = (
        ('active', "Active"),
        ('inactive', "Inactive"),
        ('stopped', "Stopped")
    )

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=24)
    token = models.CharField(max_length=32)
    status = models.CharField(choices=STATUSES, default=STATUSES[0], max_length=12)


    def __str__(self):
        return '{fN}'.format(fN=self.name)