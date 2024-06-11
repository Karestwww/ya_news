from datetime import timedelta

import pytest
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.test.client import Client

from news.models import News, Comment


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Тестовая новость',
        text='Текст тестовой новости',
    )
    return news


@pytest.fixture
def news_count_on_home_page_plus_one(db: None):
    now = timezone.now()
    many_news = [
        News(
            title=f'Тестовая новость № {number}',
            text='Текст тестовой новости № {number}',
            date=now - timedelta(days=number)
        )
        for number in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(many_news)


@pytest.fixture
def create_few_comments(author, news):
    now = timezone.now()
    for dela_day_create in range(3):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст тестового комментария {dela_day_create}',)
        comment.created = now - timedelta(days=dela_day_create)
        comment.save()


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментарий')


@pytest.fixture
def url_detail(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def url_delete(comment):
    return reverse('news:delete', args=(comment.pk,))


@pytest.fixture
def url_edit(comment):
    return reverse('news:edit', args=(comment.pk,))


@pytest.fixture
def url_home():
    return reverse('news:home')


@pytest.fixture
def url_login():
    return reverse('users:login')


@pytest.fixture
def url_logout():
    return reverse('users:logout')


@pytest.fixture
def url_signup():
    return reverse('users:signup')
