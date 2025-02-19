from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from datetime import datetime
from .constants import (MAX_TEXT_LENGTH, MAX_SLUG_LENGTH)

User = get_user_model()


class BaseModelForCategoriesAndGenres(models.Model):
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


class BaseModelForReviewsAndComments(models.Model):
    """Описание базовой модели для наследования для Reviews и Comments"""
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
    )

    class Meta:
        abstract = True


class Categories(BaseModelForCategoriesAndGenres):
    """Модель представления категории."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'категории'


class Genres(BaseModelForCategoriesAndGenres):
    """Модель представления жанров"""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'жанры'


class Titles(models.Model):
    """Модель представления произведения."""
    name = models.CharField(
        max_length=MAX_TEXT_LENGTH,
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        validators=[
            MaxValueValidator(datetime.now().year)
        ]
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    genres = models.ManyToManyField(
        Genres,
        related_name='titles',
        verbose_name='Жанр'
    )
    categories = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'произведения'


class Reviews(BaseModelForReviewsAndComments):
    """Модель представления отзыва к произведению."""
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
        verbose_name='Оценка'
    )
    titles = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'отзывы'


class Comments(BaseModelForReviewsAndComments):
    """Модель представления комментария к отзывам."""
    reviews = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'комментарии'