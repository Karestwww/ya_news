import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

FORM_DATA = {'text': 'Новый комментарий'}
FORM_DATA_WITH_BAD_WORD = {'text': f'Пишем плохие слова {BAD_WORDS[0]}'}
'''проверять случайное плохое слово считаю в корне неверным,т.к. создает
флуктуацию срабатывания при сбое в этого параметра.
Втречался такой термин - пропадающий дефект.
Он как суслик, есть проблема, но не поймать ее.
Как альтернативу вижу проверку всех плохих слов,
но в этом случае выходит другая проблема
- при большом кол-ве BAD_WORDS тест становится долгим.'''

@pytest.mark.django_db
def test_cant_create_comment_without_authorize(client, url_detail, url_login):
    comment_count_start_test = Comment.objects.count()
    response = client.post(url_detail, data=FORM_DATA)
    redirect_url = f'{url_login}?next={url_detail}'
    assertRedirects(response, redirect_url)
    comment_count = Comment.objects.count()
    assert comment_count == comment_count_start_test


def test_author_client_can_create_comment(author_client, author, news, url_detail):
    comment_count_start_test = Comment.objects.count()
    author_client.post(url_detail, data=FORM_DATA)
    comment = Comment.objects.last()
    comment_count = Comment.objects.count()
    # Проверяем, что кол-во комментариев увеличилось на 1
    assert comment_count == comment_count_start_test + 1
    assert comment.author == author
    assert comment.news == news
    assert comment.text == FORM_DATA['text']


def test_comment_without_bad_words(author_client, url_detail):
    comment_count_start_test = Comment.objects.count()
    response = author_client.post(url_detail, data=FORM_DATA_WITH_BAD_WORD)
    comment_count = Comment.objects.count()
    assert comment_count == comment_count_start_test
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )


def test_author_client_can_delete_comment(
        author_client, url_delete, create_few_comments
):
    comment_count_start_test = Comment.objects.count()
    author_client.post(url_delete)
    comment_count = Comment.objects.count()
    # Проверяем, что кол-во комментариев уменьшилось на 1
    assert comment_count == comment_count_start_test - 1


def test_author_client_can_edit_comment(
        author_client, url_edit, comment, create_few_comments
):
    comment_count_start_test = Comment.objects.count()
    comment_old = Comment.objects.get(id=comment.id)
    author_client.post(url_edit, data=FORM_DATA)
    comment_new = Comment.objects.get(id=comment.id)
    comment_count = Comment.objects.count()
    assert comment_count == comment_count_start_test
    assert comment_new.author == comment_old.author
    assert comment_new.news == comment_old.news
    assert not comment_new.text == comment_old.text
    assert comment_new.text == FORM_DATA['text']


def test_not_author_client_cant_delete_comment(
        not_author_client, url_delete, create_few_comments
):
    comment_count_start_test = Comment.objects.count()
    not_author_client.post(url_delete)
    comment_count = Comment.objects.count()
    assert comment_count == comment_count_start_test


def test_not_author_client_cant_edit_comment(
        not_author_client, url_edit, comment, create_few_comments
):
    comment_count_start_test = Comment.objects.count()
    comment_old = Comment.objects.get(id=comment.id)
    not_author_client.post(url_edit, data=FORM_DATA)
    comment_new = Comment.objects.get(id=comment.id)
    comment_count = Comment.objects.count()
    assert comment_count == comment_count_start_test
    assert comment_new.author == comment_old.author
    assert comment_new.news == comment_old.news
    assert comment_new.text == comment_old.text
    assert not comment_new.text == FORM_DATA['text']
