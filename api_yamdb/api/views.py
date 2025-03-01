import django_filters
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   DestroyModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet

from reviews.models import Category, Genre, Title, Review
from .permissions import IsAdminOrReadOnly, \
    IsAuthUserOrAuthorOrModerOrAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          TitleRatingSerializer, ReviewSerializer,
                          CommentSerializer)


class ListCreateDestroyViewSet(
    ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet
):
    """
    Класс для наследования во ViewSet для реализации просмотра списка обьектов,
    создания и удаления.
    """


class CategoryViewSet(ListCreateDestroyViewSet):
    """ViewSet для категории наследуемый от ListCreateDestroyViewSet."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'delete']
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    """ViewSet для жанров наследуемый от ListCreateDestroyViewSet."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'delete']
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для произведений."""
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Функция выбирает сериализатов в зависимости от действия."""
        if self.action == 'list' or self.action == 'retrieve':
            return TitleRatingSerializer
        else:
            return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthUserOrAuthorOrModerOrAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        """
        Возвращает произведение, если произведение не найдено, то ошибку 404.
        """
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title

    def get_queryset(self):
        """Возвращает отзывы произведения."""
        queryset = self.get_title().reviews.all()
        return queryset

    def perform_create(self, serializer):
        """
        Создает новый отзыв, если отзыв пользователя уже есть,
        то выводит ошибку.
        """
        title = self.get_title()
        author = self.request.user
        if Review.objects.filter(title=title, author=author).exists():
            raise ValidationError(
                'Пользователь уже оставлял отзыв на данное произведение!'
            )
        serializer.save(author=author, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthUserOrAuthorOrModerOrAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        """Возвращает ревью, если ревью не найдено, то ошибку 404."""
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review

    def get_queryset(self):
        """Возвращает комментарии к отзыву."""
        queryset = self.get_review().comments.all()
        return queryset

    def perform_create(self, serializer):
        """Сохраняет новый комментарий."""
        author = self.request.user
        review = self.get_review()
        serializer.save(author=author, review=review)
