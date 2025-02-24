from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, Title, Review, Comment

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
            )
        ]

    def validate_score(self, value):
        """Функция проверяет, что отзыв больше 1 и меньше 10."""
        if value < 1 or value > 10:
            raise serializers.ValidationError(
                'Оценка не может быть меньше 1 или больше 10'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class TitleRatingSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title c указанием рейтинга."""
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "id", "name", "year", "rating", "description", "genre", "category"
        )
        model = Title

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return None
        score = 0
        for review in reviews:
            score += review.score
        average_rating = round(score / len(reviews))
        return average_rating


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        from django.utils import timezone
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError('Указан год из будущего')
        if value <= 0:
            raise serializers.ValidationError(
                'Год не может быть равен либо меньше 0')
        return value
