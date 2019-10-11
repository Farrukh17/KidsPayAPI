from django.contrib import admin
from .models import Transaction
from .list_filters import GroupsListFilter, ChildrenListFilter


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('child', 'amount', 'paymentTime', 'paymentMethod')
    list_filter = ('paymentMethod', GroupsListFilter, ChildrenListFilter)
    search_fields = ('child__firstName', 'child__lastName', 'child__middleName', 'amount', 'paymentTime')
    raw_id_fields = ('child', )
    exclude = ['school', ]

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
