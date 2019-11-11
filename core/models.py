from django.utils.formats import number_format
from django.db import models
from django.utils.timezone import localtime
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from core.signals import repayment_day_changed


class Child(models.Model):
    CHILD_STATUSES = (
        ('active', 'Active'),
        ('deleted', 'Deleted')
    )
    id = models.CharField(primary_key=True, max_length=10)
    firstName = models.CharField(max_length=30, verbose_name='Имя')
    middleName = models.CharField(max_length=30, blank=True)
    lastName = models.CharField(max_length=30, verbose_name='Фамилия')
    group = models.ForeignKey('Group', related_name='children', on_delete=models.CASCADE, null=True, verbose_name='Группа')
    enteredDate = models.DateField(default=localtime().now, verbose_name='Дата вступления')
    father = models.CharField(max_length=100, blank=True, verbose_name='Отец')
    contactFather = models.CharField(max_length=12, blank=True, verbose_name='Контактный телефон отца')
    mother = models.CharField(max_length=100, blank=True, verbose_name='Мать')
    contactMother = models.CharField(max_length=12, blank=True, verbose_name='Контактный телефон матери')
    monthlyFee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Ежемесячный взнос')
    agreementNumber = models.CharField(max_length=20, verbose_name='Номер и дата договора')
    birthCertificateNumber = models.CharField(max_length=20, default='', verbose_name='Номер свидетельства о рождении')
    school = models.ForeignKey('School', on_delete=models.CASCADE, related_name='children', null=True, verbose_name='Детский садик')
    balance = models.DecimalField(max_digits=12, default=0.00, decimal_places=2, verbose_name='Баланс')
    status = models.CharField(max_length=12, choices=CHILD_STATUSES, default=CHILD_STATUSES[0][0])
    child_number = models.CharField(max_length=4, blank=True, null=True, verbose_name='Воспитанник ID')
    created_date = models.DateField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Воспитанник'
        verbose_name_plural = 'Воспитанники'

    def __str__(self):
        return '{fN} {lN} {mN}'.format(fN=self.firstName, mN=self.middleName, lN=self.lastName).strip()

    @property
    def last_payment_date(self):
        last_tr = self.transactions.latest('paymentTime')
        if not last_tr:
            return ''
        else:
            return last_tr.paymentTime.strftime('%d.%m.%Y')

    @property
    def last_payment_amount(self):
        last_tr = self.transactions.latest('paymentTime')
        if not last_tr:
            return ''
        else:
            return str(number_format(last_tr.amount, 0)) + ' UZS'


def get_logo_upload_folder(instance, filename):
    return 'logos/{school}/{filename}'.format(school=instance.name, filename=filename)


class School(models.Model):
    DEFAULT_LOGO = 'default_logo.png'
    STATUSES = (
        ('active', "Active"),
        ('inactive', "Inactive"),
        ('stopped', "Stopped")
    )
    id = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Детский садик')
    logo = models.ImageField(upload_to=get_logo_upload_folder, verbose_name='Лого', null=True, blank=True, default=DEFAULT_LOGO)
    bankAccount = models.CharField(max_length=20, verbose_name='Счет')
    taxNumber = models.CharField(max_length=9, verbose_name='ИНН')
    mfo = models.CharField(max_length=5, verbose_name='МФО Банка')
    directorName = models.CharField(max_length=100, verbose_name='Ф.И.О. директора')
    contactDirector = models.CharField(max_length=12, verbose_name='Контактный номер директора', help_text='Например: 998901234567')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    status = models.CharField(choices=STATUSES, default=STATUSES[0][0], max_length=12, verbose_name='Статус')
    agreementDocNumber = models.CharField(max_length=30, blank=True, verbose_name='Номер договора')
    repaymentDate = models.SmallIntegerField(default=1, verbose_name='Дата перерасчета')
    created_date = models.DateField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Детский садик'
        verbose_name_plural = 'Детские садики'

    def __str__(self):
        return '{name}'.format(name=self.name)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        try:
            old_school = School.objects.get(id=self.id)
            if old_school.repaymentDate != self.repaymentDate:
                repayment_day_changed.send(sender=self.__class__, prev_repayment_date=old_school.repaymentDate,
                                           new_repayment_date=self.repaymentDate, instance=self)
        except ObjectDoesNotExist:
            pass
        except MultipleObjectsReturned:
            pass

        super(School, self).save(force_insert, force_update, using, update_fields)

    def clean(self):
        try:
            if not self.id:
                n = str(int(School.objects.latest('id').id) + 1)
                self.id = n.zfill(5)
        except ObjectDoesNotExist:
            self.id = '00001'


class Group(models.Model):
    GROUP_STATUSES = (
        ('active', 'Active'),
        ('deleted', 'Deleted')
    )
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, verbose_name='Название группы')
    fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='Ежемесячный взнос')
    maxNumberOfChild = models.SmallIntegerField(blank=True, default=20, verbose_name='Максимальное количество детей')
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name='Детский садик')
    status = models.CharField(max_length=12, choices=GROUP_STATUSES, default=GROUP_STATUSES[0][0])
    created_date = models.DateField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        # default_permissions = ()
        # permissions = (
        #     ('add_core_group', 'Can add Группа'),
        #     ('change_core_group', 'Can change Группа'),
        #     ('delete_core_group', 'Can delete Группа'),
        #     ('view_core_group', 'Can view Группа'),
        # )

    def __str__(self):
        return '{name}'.format(name=self.name)

    def clean(self):
        if not self.id:
            try:
                self.id = Group.objects.latest('id').id + 1
            except ObjectDoesNotExist:
                self.id = 1

# TODO export to XLS file in one button
# TODO if possible formatting the amount field


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
    created_date = models.DateField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Приложение'
        verbose_name_plural = 'Приложения'

    def __str__(self):
        return '{name}'.format(name=self.name)

    def clean(self):
        if not self.id:
            try:
                self.id = App.objects.latest('id').id + 1
            except ObjectDoesNotExist:
                self.id = 1


class Admin(AbstractUser):
    ADMIN_TYPES = (
        ('superuser', 'SuperUser'),
        ('admin', 'Admin'),
        ('director', 'Director'),
        ('accountant', 'Accountant')
    )
    type = models.CharField(choices=ADMIN_TYPES, default=ADMIN_TYPES[1][0], max_length=12, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
