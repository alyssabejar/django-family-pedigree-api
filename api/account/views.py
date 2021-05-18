from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.status import *

from .models import Account
from .serializers import \
    (
    AccountSerializer,
    UserAccountSerializer,
)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all().order_by('created_at')
    serializer_class = AccountSerializer

    @action(methods=['POST', 'GET'], detail=False)
    def get_account_from_user_id(self, request):
        data = request.data
        user_id = data.get('user_id')

        account = Account.objects.filter(user_id=user_id).first()
        serializer = AccountViewSet.serializer_class(account)

        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def create_account(self, request):
        data = request.data
        user_id = data.get('user_id')
        dob = data.get('dob')

        # Get User via ID
        user = User.objects.filter(id=user_id).order_by("pk").first()

        if not user:
            return Response({
                'status': HTTP_400_BAD_REQUEST,
                'message': 'ERROR: User ID does not exist.',
            }, status=HTTP_400_BAD_REQUEST)

        # Create User's Account
        account = Account.objects.create(user=user, dob=dob)

        if account:
            serializer = AccountViewSet.serializer_class(account)
            return Response(serializer.data)

        return Response({
            'status': HTTP_400_BAD_REQUEST,
            'message': 'ERROR: Cannot create Account',
        }, status=HTTP_400_BAD_REQUEST)


class UserAccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all().order_by('id')
    serializer_class = UserAccountSerializer


