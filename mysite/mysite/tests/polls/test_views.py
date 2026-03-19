import datetime

import pytest
from django.urls import reverse
from django.utils import timezone
from polls.models import Choice, Question


@pytest.mark.django_db
def test_index_returns_latest_five_questions_ordered_desc(client):
    # Given
    now = timezone.now()
    for index in range(6):
        Question.objects.create(
            question_text=f"Question {index}",
            pub_date=now - datetime.timedelta(hours=index),
        )

    # When
    response = client.get(reverse("polls:index"))

    # Then
    questions = list(response.context["latest_question_list"])
    assert response.status_code == 200
    assert len(questions) == 5
    assert questions[0].pub_date > questions[-1].pub_date


@pytest.mark.django_db
def test_detail_returns_question_page(client):
    # Given
    question = Question.objects.create(
        question_text="Question detail",
        pub_date=timezone.now(),
    )

    # When
    response = client.get(reverse("polls:detail", args=[question.id]))

    # Then
    assert response.status_code == 200
    assert "Question detail" in response.content.decode()


@pytest.mark.django_db
def test_detail_returns_404_for_unknown_question(client):
    # Given
    invalid_question_id = 9999

    # When
    response = client.get(reverse("polls:detail", args=[invalid_question_id]))

    # Then
    assert response.status_code == 404


@pytest.mark.django_db
def test_results_returns_question_results_page(client):
    # Given
    question = Question.objects.create(
        question_text="Results question",
        pub_date=timezone.now(),
    )

    # When
    response = client.get(reverse("polls:results", args=[question.id]))

    # Then
    assert response.status_code == 200
    assert "Results question" in response.content.decode()


@pytest.mark.django_db
def test_vote_without_choice_redisplays_form_with_error_message(client):
    # Given
    question = Question.objects.create(
        question_text="Vote question",
        pub_date=timezone.now(),
    )
    choice = Choice.objects.create(question=question, choice_text="Option A")

    # When
    response = client.post(reverse("polls:vote", args=[question.id]), data={})

    # Then
    choice.refresh_from_db()
    content = response.content.decode()
    assert response.status_code == 200
    assert "select a choice" in content
    assert choice.votes == 0


@pytest.mark.django_db
def test_vote_with_valid_choice_increments_votes_and_redirects(client):
    # Given
    question = Question.objects.create(
        question_text="Vote question",
        pub_date=timezone.now(),
    )
    choice = Choice.objects.create(question=question, choice_text="Option A", votes=0)

    # When
    response = client.post(
        reverse("polls:vote", args=[question.id]),
        data={"choice": choice.id},
    )

    # Then
    choice.refresh_from_db()
    assert response.status_code == 302
    assert response.url == reverse("polls:results", args=[question.id])
    assert choice.votes == 1
