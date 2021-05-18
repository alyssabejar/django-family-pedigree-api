from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import MemberSerializer

from .models import Member
from django.contrib.auth.models import User


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all().order_by('-created_at')
    serializer_class = MemberSerializer

