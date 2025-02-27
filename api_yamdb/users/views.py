import random
import string

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import mixins, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.constants import CONFIRMATION_CODE_LENGTH
from users.permissions import IsAdmin
from users.serializers import AdminUserSerializer, SignupSerializer, \
    TokenSerializer, UserSerializer

User = get_user_model()


def generate_confirmation_code():
    return ''.join(random.choices(string.digits, k=CONFIRMATION_CODE_LENGTH))


class SignupViewSet(viewsets.ViewSet):
    """Позволяет пользователям получить confirmation_code."""

    def create(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user, created = User.objects.get_or_create(
                username=serializer.validated_data['username'],
                defaults={'email': serializer.validated_data['email']}
            )
            if not created and user.email != serializer.validated_data['email']:
                return Response(
                    {
                        'email': [user.email],
                        'username': [user.username]
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            if created and User.objects.filter(
                    email=serializer.validated_data['email']
                    ).exclude(username=user.username).exists():
                return Response(
                    serializer.data,
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.confirmation_code = generate_confirmation_code()
            user.save()

            send_mail(
                subject='Ваш код подтверждения',
                message=f'Ваш код: {user.confirmation_code}',
                from_email='admin@yamdb.ru',
                recipient_list=(user.email,),
                fail_silently=True,
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenViewSet(viewsets.ViewSet):
    """Получение JWT-токена после подтверждения email."""

    def create(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']
            user = get_object_or_404(User, username=username)
            if user.confirmation_code == confirmation_code:
                token = AccessToken.for_user(user)
                return Response(
                    {'token': str(token)},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'error': 'Неверный код подтверждения'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """Позволяет пользователю обновить свой профиль."""

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class AdminUserViewSet(viewsets.ModelViewSet):
    """Управление пользователями администратором."""

    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', 'email')
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']
