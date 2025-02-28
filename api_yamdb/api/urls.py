from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, CommentViewSet, GenreViewSet, \
    ReviewViewSet, TitleViewSet
from users.views import AdminUserViewSet, SignupViewSet, TokenViewSet, \
    UserProfileViewSet

router_v1 = DefaultRouter()

router_v1.register('auth/signup', SignupViewSet, basename='signup')
router_v1.register('auth/token', TokenViewSet, basename='token')
router_v1.register('users', AdminUserViewSet, basename='admin-users')

router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews-list'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments-list'
)
v1_api_urls = [
    path(
        'users/me/',
        UserProfileViewSet.as_view({'get': 'retrieve', 'patch': 'update'}),
        name='user-profile'
    ),
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(v1_api_urls)),
]
