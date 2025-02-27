from django.core.management.base import BaseCommand
import csv
from django.conf import settings
from reviews.models import Category, Review, Genre, Title, Comment, User


class Command(BaseCommand):
    """Класс для импорта данных из CSV файлов."""
    help = 'Импортирует файлы csv с данными'

    def handle(self, *args, **options):
        dir_place = settings.BASE_DIR / 'static' / 'data'

        with open(dir_place / 'category.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')
            Category.objects.all().delete()
            self.stdout.write('Начало импорта данных Category')
            for row in reader:
                try:
                    Category.objects.create(
                        id=row['id'],
                        name=row['name'],
                        slug=row['slug'],
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Ошибка импорта Category: {e}')
                    )
            else:
                self.stdout.write(
                    self.style.SUCCESS('Импорт данных для Category завершён')
                )

        with open(dir_place / 'genre.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')
            Genre.objects.all().delete()
            self.stdout.write('Начало импорта данных Genre')
            for row in reader:
                try:
                    Genre.objects.create(
                        id=row['id'],
                        name=row['name'],
                        slug=row['slug'],
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Ошибка импорта Genre: {e}')
                    )
            else:
                self.stdout.write(
                    self.style.SUCCESS('Импорт данных для Genre завершён')
                )

        with open(dir_place / 'titles.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')
            Title.objects.all().delete()
            self.stdout.write('Начало импорта данных Title')
            for row in reader:
                try:
                    Title.objects.create(
                        id=row['id'],
                        name=row['name'],
                        year=row['year'],
                        category_id=row['category'],
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Ошибка импорта Title: {e}')
                    )
            else:
                self.stdout.write(
                    self.style.SUCCESS('Импорт данных для Title завершён')
                )

        with open(dir_place / 'users.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')
            User.objects.all().delete()
            self.stdout.write('Начало импорта данных User')
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
                    self.stdout.write(
                        self.style.ERROR(f'Ошибка импорта User: {e}')
                    )
            else:
                self.stdout.write(
                    self.style.SUCCESS('Импорт данных для User завершён')
                )

        with open(dir_place / 'review.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')
            Review.objects.all().delete()
            self.stdout.write('Начало импорта данных Review')
            for row in reader:
                try:
                    Review.objects.create(
                        id=row['id'],
                        title_id=row['title_id'],
                        text=row['text'],
                        author_id=row['author'],
                        score=row['score'],
                        pub_date=row['pub_date'],
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Ошибка импорта Review: {e}')
                    )
            else:
                self.stdout.write(
                    self.style.SUCCESS('Импорт данных для Review завершён')
                )

        with open(dir_place / 'comments.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')
            Comment.objects.all().delete()
            self.stdout.write('Начало импорта данных Comment')
            for row in reader:
                try:
                    Comment.objects.create(
                        id=row['id'],
                        review_id=row['review_id'],
                        text=row['text'],
                        author_id=row['author'],
                        pub_date=row['pub_date'],
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Ошибка импорта Comment: {e}')
                    )
            else:
                self.stdout.write(
                    self.style.SUCCESS('Импорт данных для Comment завершён')
                )

        with (open(dir_place / 'genre_title.csv', 'r', encoding='utf-8')
              as file):
            reader = csv.DictReader(file, delimiter=',')
            self.stdout.write('Начало импорта данных Genre_Title')
            for row in reader:
                try:
                    title = Title.objects.get(id=row['title_id'])
                    genre = Genre.objects.get(id=row['genre_id'])
                    title.genre.add(genre)
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Ошибка импорта Genre_Title: {e}')
                    )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        'Импорт данных для Genre_Title завершён'
                    )
                )
