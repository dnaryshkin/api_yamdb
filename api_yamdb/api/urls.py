from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import SignupViewSet, TokenViewSet, UserProfileViewSet, AdminUserViewSet

# from api.views import CommentViewSet, FollowViewSet, GroupViewsSet, PostViewSet

router_v1 = routers.DefaultRouter()
# router_v1.register(
#     'posts',
#     PostViewSet,
#     basename='posts'
# )
# router_v1.register(
#     'groups',
#     GroupViewsSet,
#     basename='groups'
# )
# router_v1.register(
#     r'posts/(?P<post>\d+)/comments',
#     CommentViewSet,
#     basename='comments'
# # )

router_v1.register(r'auth/signup', SignupViewSet, basename='signup')
router_v1.register(r'auth/token', TokenViewSet, basename='token')
router_v1.register(r'users/me', UserProfileViewSet, basename='user-profile')
router_v1.register(r'users', AdminUserViewSet, basename='admin-users')

v1_api_urls = [
    # path('', include('djoser.urls.jwt')),
    path('', include(router_v1.urls)),

    # path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]

urlpatterns = [
    path('v1/', include(v1_api_urls)),
]
