from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Account

Account = get_user_model()

class AccountSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Account
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'password']