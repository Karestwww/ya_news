from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture as lf



@pytest.mark.parametrize(
    'url, client_tested, status',
    (
        (lf('url_home'), lf('client'), HTTPStatus.OK),
        (lf('url_login'), lf('client'), HTTPStatus.OK),
        (lf('url_logout'), lf('client'), HTTPStatus.OK),
        (lf('url_signup'), lf('client'), HTTPStatus.OK),
        (lf('url_detail'), lf('client'), HTTPStatus.OK),
        (lf('url_delete'), lf('author_client'), HTTPStatus.OK),
        (lf('url_edit'), lf('author_client'), HTTPStatus.OK),
        (lf('url_delete'), lf('not_author_client'), HTTPStatus.NOT_FOUND),
        (lf('url_edit'), lf('not_author_client'), HTTPStatus.NOT_FOUND),
    )
)
@pytest.mark.django_db(True)
def test_home_availability_for_anonymous_user(url, client_tested, status):
    response = client_tested.get(url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'url',
    (lf('url_delete'), lf('url_edit'),)
)
@pytest.mark.django_db(True)
def test_revers_edit_delete_comment_user_not_authorized(
    client, url, url_login, create_few_comments
):
    response = client.get(url)
    redirect_url = f'{url_login}?next={url}'
    assertRedirects(response, redirect_url)
