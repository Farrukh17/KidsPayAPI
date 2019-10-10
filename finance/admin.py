from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('child', 'amount', 'paymentTime', 'paymentMethod')
    list_filter = ('paymentMethod', )
    search_fields = ('child', 'amount', 'paymentTime')
    raw_id_fields = ('child', )
