from django.contrib.auth.models import User
from rest_framework import serializers

from pedigree.serializers import MemberSerializer


class UserSerializer(serializers.ModelSerializer):
    members = MemberSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'date_joined', 'members']


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

# class UserAccountSerializer(serializers.ModelSerializer):
#     account = AccountSerializer()
#
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'first_name', 'last_name']
"""
class UserSerializerApi(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        return User().objects.create_user(**validated_data)
"""
