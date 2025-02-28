from django.contrib import admin
from .models import Category, Genre, Title, Review, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "year", "category")
    search_fields = ("name",)
    list_filter = ("year", "category")
    ordering = ("name",)
    filter_horizontal = ("genre",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "score", "pub_date")
    search_fields = ("author__username", "title__name")
    list_filter = ("score", "pub_date")
    ordering = ("-pub_date",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "review", "author", "pub_date")
    search_fields = ("author__username", "review__title")
    list_filter = ("pub_date",)
    ordering = ("-pub_date",)
