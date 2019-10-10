from rest_framework import serializers
from ..models import Child


class ChildSerializer(serializers.ModelSerializer):
    school = serializers.StringRelatedField()
    group = serializers.StringRelatedField()

    class Meta:
        model = Child
        fields = ['firstName', 'lastName', 'middleName', 'enteredDate', 'father', 'contactFather', 'mother',
                  'contactMother', 'monthlyFee', 'agreementNumber', 'birthCertificateNumber', 'school', 'group', 'debt']
