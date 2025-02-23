from django.contrib.auth import get_user_model
from django.db import models

from .constants import (MAX_TEXT_LENGTH, MAX_SLUG_LENGTH)

User = get_user_model()


class BaseModelForCategoryAndGenre(models.Model):
    """Описание базовой модели для наследования Categories и Genres"""
    name = models.CharField(
        max_length=MAX_TEXT_LENGTH,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=MAX_SLUG_LENGTH,
        unique=True,
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(BaseModelForCategoryAndGenre):
    """Модель представления категории."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'категории'


class Genre(BaseModelForCategoryAndGenre):
    """Модель представления жанров"""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'жанры'


class Title(models.Model):
    """Модель представления произведения."""
    name = models.CharField(
        max_length=MAX_TEXT_LENGTH,
        verbose_name='Название произведения'
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name
