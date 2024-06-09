from django.conf import settings
from django.urls import reverse
import pytest


@pytest.mark.parametrize(
    'name',
    (pytest.lazy_fixture('author_client'), pytest.lazy_fixture('client'))
)
def test_list_news_home_page_quantity(name, news_count_on_home_page_plus_one):
    url = reverse('news:home')
    response = name.get(url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count==settings.NEWS_COUNT_ON_HOME_PAGE
    dates_news_home_page = [news.date for news in object_list]
    sorted_dates_news_home_page = sorted(dates_news_home_page, reverse=True)
    assert sorted_dates_news_home_page==dates_news_home_page

def test_comments_corted(author_client, news, create_few_comments):
    url = reverse('news:detail', args=(news.id,))
    response = author_client.get(url)
    news = response.context['news']
    all_comments = news.comment_set.all()
    sorted_comment = sorted(all_comments, key=lambda comment: comment.created)
    assert list(all_comments) == sorted_comment

def test_form_author_client(author_client, news):
    url = reverse('news:detail', args=(news.id,))
    response = author_client.get(url)
    assert 'form' in response.context

@pytest.mark.django_db
def test_form_user_not_authorized(client, news):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert 'form' not in response.context
