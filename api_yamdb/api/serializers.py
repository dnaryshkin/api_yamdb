from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers

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
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            "id", "name", "year", "rating", "description", "genre", "category"
        )
        model = Title

    def validate(self, data):
        """Валидация что рейтинг от 1 до 10."""
        rating = data['rating']
        if rating < 1 or rating > 10:
            raise serializers.ValidationError(
                'Рейтинг должно быть целое число от 1 до 10'
            )
        return data


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

    def validate(self, data):
        """Валидация что год не больше текущего года."""
        current_year = datetime.today().year
        if 'year' in data and data['year'] > current_year:
            raise serializers.ValidationError("Год не может быть больше текущего!")
        return data
