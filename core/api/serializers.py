from django.utils.formats import number_format
from rest_framework import serializers
from ..models import Child


class ChildSerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField()
    monthly_fee = serializers.SerializerMethodField('monthlyFee_localize')
    balance = serializers.SerializerMethodField('balance_localize')
    full_name = serializers.SerializerMethodField('get_full_name')

    def monthlyFee_localize(self, obj):
        return number_format(obj.monthlyFee, 0) + ' UZS'

    def balance_localize(self, obj):
        return number_format(obj.balance, 0) + ' UZS'

    def get_full_name(self, obj):
        return obj.__str__()

    class Meta:
        model = Child
        fields = ['full_name', 'monthly_fee', 'group', 'last_payment_date', 'last_payment_amount', 'balance']
