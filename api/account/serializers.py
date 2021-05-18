from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.reverse import reverse

from .models import Account
from users.serializers import UserSerializer, UserUpdateSerializer


class AccountSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user")  # get user and display in account api

    @staticmethod
    def get_user(instance):
        serializer = UserSerializer(instance.user)
        return serializer.data

    class Meta:
        model = Account
        fields = '__all__'


class UserAccountSerializer(serializers.HyperlinkedModelSerializer):
    user = UserUpdateSerializer()

    class Meta:
        model = Account
        fields = ['id', 'dob', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        account = Account.objects.create(**validated_data)
        Account.objects.create(account=account, **user_data)
        return account

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.dob = validated_data.get('dob', instance.dob)
        instance.save()

        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.save()

        return instance
