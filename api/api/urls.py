import debug_toolbar
import pedigree

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework.status import HTTP_200_OK
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.viewsets import ViewSet

from account.views import AccountViewSet, UserAccountViewSet
from users.views import UserViewSet
from pedigree.views import MemberViewSet
from pedigree import views
from api.settings import STATIC_URL, STATIC_ROOT


class APIBaseViewSet(ViewSet):
    """ Simple API status checker """
    permission_classes = []
    authentication_classes = []

    @action(methods=['GET'], detail=False)
    def check_api_status(self, request):
        return Response(
            {"status": HTTP_200_OK, "message": "API is fully functional."},
            status=HTTP_200_OK,
            content_type="application/json"
        )


""" API Router """
router = routers.DefaultRouter()
router.register('base', APIBaseViewSet, basename='api-base')
router.register('users', UserViewSet, basename='users')
router.register('accounts', AccountViewSet, basename='accounts')
router.register('members', MemberViewSet, basename='members')
router.register('user-account', UserAccountViewSet, basename='user-account')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('openid/', include('oidc_provider.urls', namespace='oidc_provider')),
    path('__debug__/', include(debug_toolbar.urls)),

]


urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
