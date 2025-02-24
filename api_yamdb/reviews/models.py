from django.contrib.auth import get_user_model
from django.db import models

from .constants import (MAX_TEXT_LENGTH, MAX_SLUG_LENGTH)

User = get_user_model()


class BaseModelForCategoryAndGenre(models.Model):
    """Описание базовой модели для наследования Categories и Genres"""
    name = models.CharField(
        max_length=MAX_TEXT_LENGTH,
        unique=True,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=MAX_SLUG_LENGTH,
        unique=True,
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        """Возвращение названия."""
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
        verbose_name='Название произведения',
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
        verbose_name='Жанр',
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
        """Возвращение названия произведения."""
        return self.name



class Review(models.Model):
    """Модель представления отзывов"""
    text = models.TextField(
        verbose_name='Текст',
        help_text='Текст отзыва',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации отзыва',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        """Возвращение текста отзыва."""
        return self.text


class Comment(models.Model):
    """Модель представления комментариев"""
    text = models.TextField(
        verbose_name='Текст',
        help_text='Текст комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации комментария'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)

    def __str__(self):
        """Возвращение текста комментария."""
        return self.text
