import pytest
from django.conf import settings
from pytest_lazyfixture import lazy_fixture as lf

from news.forms import CommentForm


@pytest.mark.parametrize(
    'name',
    (lf('author_client'), lf('client'))
)
def test_list_news_home_page_quantity(name, url_home, news_count_on_home_page_plus_one):
    response = name.get(url_home)
    news_home_page = response.context['object_list']
    news_count = news_home_page.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE
    dates_news_home_page = [news.date for news in news_home_page]
    sorted_dates_news_home_page = sorted(dates_news_home_page, reverse=True)
    assert sorted_dates_news_home_page == dates_news_home_page


def test_comments_corted(author_client, url_detail, create_few_comments):
    response = author_client.get(url_detail)
    news = response.context['news']
    all_comments = news.comment_set.all()
    sorted_comment = sorted(all_comments, key=lambda comment: comment.created)
    assert list(all_comments) == sorted_comment


def test_form_author_client(author_client, url_detail):
    response = author_client.get(url_detail)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


@pytest.mark.django_db
def test_form_user_not_authorized(client, url_detail):
    response = client.get(url_detail)
    assert 'form' not in response.context
