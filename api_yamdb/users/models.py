from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants import MAX_TEXT_LENGTH, MAX_EMAIL_LENGTH, CONFIRMATION_CODE_LENGTH


class CustomizedUser(AbstractUser):
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
        # null=True
    )
    confirmation_code = models.CharField(
        max_length=CONFIRMATION_CODE_LENGTH,
        blank=True,
        null=True
        )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username
