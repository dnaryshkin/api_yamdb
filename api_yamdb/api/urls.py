from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, TitleViewSet, GenreViewSet
from users.views import SignupViewSet, TokenViewSet, UserProfileViewSet, AdminUserViewSet

router_v1 = DefaultRouter()

router_v1.register(r'auth/signup', SignupViewSet, basename='signup')
router_v1.register(r'auth/token', TokenViewSet, basename='token')
router_v1.register(r'users/me', UserProfileViewSet, basename='user-profile')
router_v1.register(r'users', AdminUserViewSet, basename='admin-users')

router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)

v1_api_urls = [
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(v1_api_urls)),
]
