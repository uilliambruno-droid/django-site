import datetime

import pytest
from django.utils import timezone
from polls.models import Choice, Question


@pytest.mark.django_db
def test_question_str_returns_question_text():
    # Given
    question = Question.objects.create(
        question_text="Favorite language?",
        pub_date=timezone.now(),
    )

    # When
    result = str(question)

    # Then
    assert result == "Favorite language?"


@pytest.mark.django_db
def test_choice_str_returns_question_id_and_choice_text():
    # Given
    question = Question.objects.create(
        question_text="Best framework?",
        pub_date=timezone.now(),
    )
    choice = Choice.objects.create(question=question, choice_text="Django")

    # When
    result = str(choice)

    # Then
    assert result == f"{question.id} : Django"


@pytest.mark.django_db
def test_was_published_recently_returns_true_for_recent_question():
    # Given
    question = Question.objects.create(
        question_text="Recent question",
        pub_date=timezone.now() - datetime.timedelta(hours=12),
    )

    # When
    result = question.was_published_recently()

    # Then
    assert result is True


@pytest.mark.django_db
def test_was_published_recently_returns_false_for_old_question():
    # Given
    question = Question.objects.create(
        question_text="Old question",
        pub_date=timezone.now() - datetime.timedelta(days=2),
    )

    # When
    result = question.was_published_recently()

    # Then
    assert result is False
