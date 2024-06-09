import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import WARNING
from news.models import Comment


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

def test_author_client_can_create_comment(author_client, news, form_data):
    comment_count_start_test = Comment.objects.count()
    url = reverse('news:detail', args=(news.id,))
    author_client.post(url, data=form_data)
    comment_count = Comment.objects.count()
    # Проверяем, что кол-во комментариев увеличилось на 1
    assert comment_count == comment_count_start_test + 1

def test_comment_without_bad_words(
        author_client, news, form_data_with_bad_word):
    comment_count_start_test = Comment.objects.count()
    url = reverse('news:detail', args=(news.id,))
    response = author_client.post(url, data=form_data_with_bad_word)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comment_count = Comment.objects.count()
    assert comment_count == comment_count_start_test

def test_author_client_can_delete_comment(
        author_client, form_data, news, create_few_comments
):
    comment_count_start_test = Comment.objects.count()
    url = reverse('news:delete', args=(news.pk,))
    author_client.post(url, data=form_data)
    comment_count = Comment.objects.count()
    # Проверяем, что кол-во комментариев уменьшилось на 1
    assert comment_count == comment_count_start_test - 1

def test_author_client_can_edit_comment(
        author_client, form_data, news, create_few_comments
):
    comment_count_start_test = Comment.objects.count()
    url = reverse('news:edit', args=(news.pk,))
    author_client.post(url, data=form_data)
    comment_count = Comment.objects.count()
    assert comment_count == comment_count_start_test

def test_not_author_client_can_delete_comment(
        not_author_client, form_data, news, create_few_comments
):
    comment_count_start_test = Comment.objects.count()
    url = reverse('news:delete', args=(news.pk,))
    not_author_client.post(url, data=form_data)
    comment_count = Comment.objects.count()
    assert comment_count == comment_count_start_test

def test_not_author_client_can_edit_comment(
        not_author_client, form_data, news, create_few_comments
):
    comment_count_start_test = Comment.objects.count()
    url = reverse('news:edit', args=(news.pk,))
    not_author_client.post(url, data=form_data)
    comment_count = Comment.objects.count()
    assert comment_count == comment_count_start_test
