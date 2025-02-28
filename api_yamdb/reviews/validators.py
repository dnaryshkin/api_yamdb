from datetime import datetime

from rest_framework.serializers import ValidationError


def validate_year(value):
    """Проверяет, что указанный год не больше текущего года"""
    current_year = datetime.today().year
    if value > current_year:
        raise ValidationError(
            f'Указанный год: {value} - больше текущего года: {current_year}'
        )
    return value
