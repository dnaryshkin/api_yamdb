from django.db.models import Avg
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin, \
    DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from reviews.models import Category, Genre, Title, Review, Comment
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer, \
    TitleRatingSerializer, ReviewSerializer, CommentSerializer


class ListCreateDestroyViewSet(
    ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet
):
    """
    Класс для наследования во ViewSet для реализации просмотра списка обьектов,
    создания и удаления.
    """
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    """ViewSet для категории наследуемый от ListCreateDestroyViewSet."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    """ViewSet для жанров наследуемый от ListCreateDestroyViewSet."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для произведений."""
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    ).order_by('name')

    def get_serializer_class(self):
        """Функция выбирает сериализатов в зависимости от действия."""
        if self.action in ['list', 'retrieve']:
            return TitleRatingSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer