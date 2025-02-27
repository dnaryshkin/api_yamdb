from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from users.constants import CONFIRMATION_CODE_LENGTH, MAX_EMAIL_LENGTH, \
    MAX_TEXT_LENGTH

User = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):
    """Сериализатор для управления пользователями (доступен админу)."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'role', 'first_name', 'last_name', 'bio'
        )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя (редактирование без смены роли)."""

    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'role', 'first_name', 'last_name', 'bio'
        )


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""

    username = serializers.CharField(
        max_length=MAX_TEXT_LENGTH,
        validators=(UnicodeUsernameValidator(),),
    )
    email = serializers.EmailField(max_length=MAX_EMAIL_LENGTH)

    class Meta:
        model = User
        fields = ("username", "email")

    def validate_username(self, value):
        """Проверка на неиспользование имени me."""
        if value.lower() == 'me':
            raise serializers.ValidationError('Использовать "me" запрещено!')
        return value

    def validate(self, data):
        """Проверка передаваемых имени и email."""
        username = data["username"].lower()
        email = data["email"].lower()

        if User.objects.filter(username__iexact=username).exclude(
                email__iexact=email
        ).exists():
            raise serializers.ValidationError("Этот username уже занят!")

        if User.objects.filter(email__iexact=email).exclude(
                username__iexact=username
        ).exists():
            raise serializers.ValidationError("Этот email уже используется!")
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT-токена."""

    username = serializers.CharField(max_length=MAX_TEXT_LENGTH)
    confirmation_code = serializers.CharField(
        max_length=CONFIRMATION_CODE_LENGTH
    )
