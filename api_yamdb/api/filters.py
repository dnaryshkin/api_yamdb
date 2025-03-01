from django_filters import rest_framework as filters
import django_filters
from reviews.models import Title


class TitleFilter(filters.FilterSet):
    """Класс для фильтрации произведений по жанру."""
    genre = django_filters.CharFilter(
        field_name='genre__slug',
    )
    category = django_filters.CharFilter(
        field_name='category__slug',
    )

    class Meta:
        model = Title
        fields = ('genre', 'category', 'year', 'name')
