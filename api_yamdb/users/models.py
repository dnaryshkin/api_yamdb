from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants import CONFIRMATION_CODE_LENGTH, MAX_EMAIL_LENGTH, \
    MAX_TEXT_LENGTH


class CustomizedUser(AbstractUser):
    """Измененная модель пользователей."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    role = models.CharField(
        max_length=MAX_TEXT_LENGTH,
        choices=ROLES,
        default=USER,
    )
    email = models.EmailField(
        'Email',
        max_length=MAX_EMAIL_LENGTH,
        unique=True,

    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    confirmation_code = models.CharField(
        max_length=CONFIRMATION_CODE_LENGTH,
        blank=True,
        null=True
    )

    def is_admin(self):
        """Проверка на одмина."""
        return self.role == self.ADMIN or self.is_superuser

    def is_moderator(self):
        """Проверка на модератора."""
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        default_related_name = 'users'
        ordering = ('username',)
