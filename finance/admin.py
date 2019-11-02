from django.contrib import admin
from .models import Transaction, History
from core.models import Child
from .list_filters import FinanceGroupsListFilter, ChildrenListFilter, SchoolsListFilter, GroupListFilter


class TransactionAdmin(admin.ModelAdmin):
    def get_payment_method(self, obj):
        if obj.paymentMethod == 'online':
            return obj.appType
        else:
            return obj.paymentMethod

    get_payment_method.short_description = 'МЕТОД ОПЛАТЫ'

    list_display = ('child', 'amount', 'paymentTime', 'get_payment_method')
    list_filter = ('paymentMethod', SchoolsListFilter, FinanceGroupsListFilter, ChildrenListFilter)
    search_fields = ('child__firstName', 'child__lastName', 'child__middleName', 'amount', 'paymentTime')
    autocomplete_fields = ('child',)
    exclude = ['school', 'paymentMethod', 'appType']
    date_hierarchy = 'paymentTime'
    readonly_fields = ['paymentMethod']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser and request.user.is_authenticated:
            return qs
        if request.user.is_staff and request.user.is_authenticated:
            return qs.filter(school=request.user.school)
        return None

    def save_model(self, request, obj, form, change):
        if not change:
            obj.school = request.user.school
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "group":
            if request.user.is_staff and request.user.is_authenticated:
                kwargs["queryset"] = Child.objects.filter(school=request.user.school)
            elif request.user.is_superuser:
                kwargs["queryset"] = Child.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class HistoryAdmin(admin.ModelAdmin):
    def group(self, obj):
        return obj.child.group

    list_display = ['date', 'child', 'debitAmount', 'group']
    date_hierarchy = 'date'
    search_fields = ['group', 'debitAmount', 'child__firstName', 'child__lastName', 'child__middleName']
    list_filter = ('school__name', GroupListFilter, 'child')


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(History, HistoryAdmin)
