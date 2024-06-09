from http import HTTPStatus

from django.urls import reverse
import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

BAD_FORM_DATA = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}


@pytest.mark.django_db
def test_cant_create_comment_without_authorize(client, news, form_data):
    comment_count_start_test = Comment.objects.count()
    url = reverse('news:detail', args=(news.id,))
    url_login = reverse('users:login')
    response = client.post(url, data=form_data)
    redirect_url = f'{url_login}?next={url}'
    assertRedirects(response, redirect_url)
    comment_count = Comment.objects.count()
    assert comment_count == comment_count_start_test
    breakpoint()
