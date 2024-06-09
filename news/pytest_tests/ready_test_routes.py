from http import HTTPStatus
from django.urls import reverse
import pytest
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'name',
    (
        'news:home',
        'users:login',
        'users:logout',
        'users:signup',
    )
)
@pytest.mark.django_db(True)
def test_home_availability_for_anonymous_user(client, name):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK

@pytest.mark.django_db(True)
def test_home_url_user_not_authorized(client, news):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK

@pytest.mark.parametrize(
    'name',
    (
        'news:delete',
        'news:edit'
    )
)
def test_pages_availability_for_author_client(
        author_client, name, news, create_few_comments
):
    url = reverse(name, args=(news.pk,))
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK

@pytest.mark.parametrize(
    'name',
    (
        'news:delete',
        'news:edit'
    )
)
@pytest.mark.django_db(True)
def test_revers_edit_delete_comment_user_not_authorized(
    client, name, news, create_few_comments
):
    url = reverse(name, args=(news.pk,))
    url_login = reverse('users:login')
    response = client.get(url)
    redirect_url = f'{url_login}?next={url}'
    assertRedirects(response, redirect_url)

@pytest.mark.parametrize(
    'name',
    (
        'news:delete',
        'news:edit'
    )
)
def test_pages_availability_for_not_author_client(
        not_author_client, name, news, create_few_comments
):
    url = reverse(name, args=(news.pk,))
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
