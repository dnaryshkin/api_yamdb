from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from users.constants import CONFIRMATION_CODE_LENGTH, MAX_TEXT_LENGTH, MAX_EMAIL_LENGTH

User = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):
    """Сериализатор для управления пользователями (доступен админу)."""
    # bio = serializers.CharField(allow_blank=True, allow_null=True, default="")
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'first_name', 'last_name', 'bio')



class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя (редактирование без смены роли)."""
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'first_name', 'last_name', 'bio')


class SignupSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя."""
    username = serializers.CharField(
        max_length=MAX_TEXT_LENGTH,
        validators=[UnicodeUsernameValidator()],
    )
    email = serializers.EmailField(max_length=MAX_EMAIL_LENGTH)

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if username.lower() == 'me':
            raise serializers.ValidationError(
                {'username': 'Использовать "me" запрещено!'}
                )
        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()

        if user_by_username and user_by_username.email != email:
            raise serializers.ValidationError({"username": "Этот username уже занят!"})

        if user_by_email and user_by_email.username != username:
            raise serializers.ValidationError({"email": "Этот email уже используется!"})

        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT-токена."""

    username = serializers.CharField(max_length=MAX_TEXT_LENGTH)
    confirmation_code = serializers.CharField(max_length=CONFIRMATION_CODE_LENGTH)
