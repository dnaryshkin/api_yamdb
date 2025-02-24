from re import error

from django.core.management.base import BaseCommand
import csv
from django.conf import settings
from reviews.models import Category, Review, Genre, Title, Comment, User


class Command(BaseCommand):
    """Класс для импорта данных из CSV файлов."""
    help = 'Импортирует файлы csv с данными'

    def handle(self, *args, **options):
        dir_place = settings.BASE_DIR / 'static'/'data'

        with open(dir_place/'category.csv', 'r', encoding='utf-8') as category_file:
            reader = csv.DictReader(category_file, delimiter=',')
            error = False
            print('Начало импорта данных Сategory')
            for row in reader:
                try:
                    Category.objects.create(
                        id=row['id'],
                        name=row['name'],
                        slug=row['slug'],
                    )
                except Exception as e:
                    print(f'Возникла ошибка импорта Сategory {e}')
                    error = True
            if error == False:
                print('Выполнен импорт данных для Сategory')


        with open(dir_place/'comments.csv', 'r', encoding='utf-8') as comment_file:
            reader = csv.DictReader(comment_file, delimiter=',')
            print('Начало импорта данных Comment')
            for row in reader:
                try:
                    Comment.objects.create(
                        id=row['id'],
                        review_id=row['review_id'],
                        text=row['text'],
                        author=row['author'],
                        pub_date=row['pub_date'],
                    )
                except Exception as e:
                    print(f'Возникла ошибка импорта Comment {e}')
            print('Выполнен импорт данных для Comment')


        with open(dir_place/'genre.csv', 'r', encoding='utf-8') as genre_file:
            reader = csv.DictReader(genre_file, delimiter=',')
            print('Начало импорта данных Genre')
            for row in reader:
                try:
                    Genre.objects.create(
                        id=row['id'],
                        name=row['name'],
                        slug=row['slug'],
                    )
                except Exception as e:
                    print(f'Возникла ошибка импорта Genre {e}')
            print('Выполнен импорт данных для Genre')


        with open(dir_place/'genre_title.csv', 'r', encoding='utf-8') as genre_title_file:
            reader = csv.DictReader(genre_title_file, delimiter=',')
            print('Начало импорта данных Genre_Title')
            for row in reader:
                try:
                    title = Title.objects.get(id=row['title_id'])
                    genre = Genre.objects.get(id=row['genre_id'])
                    title.genre.add(genre)
                except Exception as e:
                    print(f'Возникла ошибка импорта Genre_Title {e}')
            print('Выполнен импорт данных для Genre_Title')


        with open(dir_place/'review.csv', 'r', encoding='utf-8') as review_file:
            reader = csv.DictReader(review_file, delimiter=',')
            print('Начало импорта данных Review')
            for row in reader:
                try:
                    Review.objects.create(
                        id=row['id'],
                        title_id=row['title_id'],
                        text=row['text'],
                        author=row['author'],
                        score=row['score'],
                        pub_date=row['pub_date'],
                    )
                except Exception as e:
                    print(f'Возникла ошибка импорта Review {e}')
            print('Выполнен импорт данных для Review')


        with open(dir_place/'titles.csv', 'r', encoding='utf-8') as title_file:
            reader = csv.DictReader(title_file, delimiter=',')
            print('Начало импорта данных Title')
            for row in reader:
                try:
                    Title.objects.create(
                        id=row['id'],
                        name=row['name'],
                        year=row['year'],
                        category=row['category'],
                    )
                except Exception as e:
                    print(f'Возникла ошибка импорта Review {e}')
            print('Выполнен импорт данных для Review')


        with open(dir_place/'users.csv', 'r', encoding='utf-8') as user_file:
            reader = csv.DictReader(user_file, delimiter=',')
            print('Начало импорта данных User')
            for row in reader:
                try:
                    User.objects.create(
                        id=row['id'],
                        username=row['username'],
                        email=row['email'],
                        role=row['role'],
                        bio=row['bio'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                    )
                except Exception as e:
                    print(f'Возникла ошибка импорта User {e}')
            print('Выполнен импорт данных для User')