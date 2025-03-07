
from iam.models import IamUser
from rest_framework import serializers


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = IamUser
        fields = ['email', 'password']

