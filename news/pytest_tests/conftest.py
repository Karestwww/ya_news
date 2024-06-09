import pytest
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from django.test.client import Client

from news.forms import BAD_WORDS
from news.models import News, Comment


@pytest.fixture
def author(django_user_model):  
    return django_user_model.objects.create(username='Автор')

@pytest.fixture
def not_author(django_user_model):  
    return django_user_model.objects.create(username='Не автор')

@pytest.fixture
def author_client(author):  # Вызываем фикстуру автора.
    # Создаём новый экземпляр клиента, чтобы не менять глобальный.
    client = Client()
    client.force_login(author)  # Логиним автора в клиенте.
    return client

@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)  # Логиним обычного пользователя в клиенте.
    return client

@pytest.fixture
def news():
    news = News.objects.create(  # Создаём новость.
        title='Тестовая новость',
        text='Текст тестовой новости',
    )
    return news

@pytest.fixture
def news_count_on_home_page_plus_one(db: None):
    return [
        News.objects.create(
        title=f'Тестовая новость № {number}',
        text='Текст тестовой новости № {number}')
        for number in range(settings.NEWS_COUNT_ON_HOME_PAGE+1)
    ]

@pytest.fixture
def create_few_comments(author, news):
    now = timezone.now()
    for dela_day_create in range(3):
        comment = Comment.objects.create(  # Создаём комментарий.
            news=news,
            author=author,
            text=f'Текст тестового комментария {dela_day_create}',)
        comment.created = now - timedelta(days=dela_day_create)
        comment.save()

@pytest.fixture
def form_data():
    return {'text': 'Новый комментарий'}

@pytest.fixture
def form_data_with_bad_word():
    return {'text': f'Пишем плохие слова {BAD_WORDS[0]}'}
