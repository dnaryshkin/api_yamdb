from django.urls import include, path
from rest_framework import routers

from users.views import SignupViewSet, TokenViewSet, UserProfileViewSet, AdminUserViewSet

router_v1 = routers.DefaultRouter()

router_v1.register(r'auth/signup', SignupViewSet, basename='signup')
router_v1.register(r'auth/token', TokenViewSet, basename='token')
router_v1.register(r'users', AdminUserViewSet, basename='admin-users')

v1_api_urls = [
    path('users/me/', UserProfileViewSet.as_view({'get': 'retrieve', 'patch': 'update'}), name='user-profile'),
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(v1_api_urls)),
]
