from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from users.constants import CONFIRMATION_CODE_LENGTH, MAX_TEXT_LENGTH, MAX_EMAIL_LENGTH

User = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):
    """Сериализатор для управления пользователями (доступен админу)."""

    class Meta:
        model = User
        exclude = ('confirmation_code',)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя (редактирование без смены роли)."""
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        exclude = ('confirmation_code',)


class SignupSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя."""
    username = serializers.CharField(
        max_length=MAX_TEXT_LENGTH,
        validators=[UnicodeUsernameValidator()],
    )
    email = serializers.EmailField(max_length=MAX_EMAIL_LENGTH)

    def validate(self, data):
        user = User.objects.filter(username=data['username']).first()
        if user and user.email != data['email']:
            raise serializers.ValidationError({'username': 'Username уже занят другим email.'})
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT-токена."""

    username = serializers.CharField(max_length=MAX_TEXT_LENGTH)
    confirmation_code = serializers.CharField(max_length=CONFIRMATION_CODE_LENGTH)
