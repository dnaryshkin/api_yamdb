from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .constants import (MAX_TEXT_LENGTH, MAX_SLUG_LENGTH)
from .validators import validate_year

User = get_user_model()


class Category(models.Model):
    """Модель представления категории."""
    name = models.CharField(
        max_length=MAX_TEXT_LENGTH,
        unique=True,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=MAX_SLUG_LENGTH,
        unique=True,
        verbose_name='Слаг',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'категории'
        ordering = ('name',)

    def __str__(self):
        """Возвращает название категории"""
        return f'Название категории: {self.name}'


class Genre(models.Model):
    """Модель представления жанров"""
    name = models.CharField(
        max_length=MAX_TEXT_LENGTH,
        unique=True,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=MAX_SLUG_LENGTH,
        unique=True,
        verbose_name='Слаг',
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'жанры'
        ordering = ('name',)

    def __str__(self):
        """Возвращает название жанра"""
        return f'Название жанра: {self.name}'


class Title(models.Model):
    """Модель представления произведения."""
    name = models.CharField(
        max_length=MAX_TEXT_LENGTH,
        verbose_name='Название произведения',
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=[
            MaxValueValidator(validate_year),
        ]
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
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
        ordering = ('name',)

    def __str__(self):
        """Возвращение названия произведения."""
        return f'Название произведения: {self.name}'


class Review(models.Model):
    """Модель представления отзывов"""
    text = models.TextField(
        verbose_name='Текст',
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
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации отзыва',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title',
            )
        ]

    def __str__(self):
        """Возвращение текста отзыва."""
        return f'Отзыв: {self.text}'


class Comment(models.Model):
    """Модель представления комментариев"""
    text = models.TextField(
        verbose_name='Текст',
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
        return f'Комментарий: {self.text}'
