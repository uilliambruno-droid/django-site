import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_login_get_renders_form_without_error_message(client):
    # Given
    url = reverse("accounts:login")

    # When
    response = client.get(url)

    # Then
    content = response.content.decode()
    assert response.status_code == 200
    assert "Login" in content
    assert "Invalid username or password" not in content


@pytest.mark.django_db
def test_login_post_invalid_credentials_shows_error_message(client):
    # Given
    url = reverse("accounts:login")

    # When
    response = client.post(url, data={"username": "invalid", "password": "invalid"})

    # Then
    assert response.status_code == 200
    assert "Invalid username or password" in response.content.decode()


@pytest.mark.django_db
def test_login_post_valid_credentials_redirects_to_contacts_create(client):
    # Given
    user = User.objects.create_user(username="valid_user", password="valid_pass123")
    url = reverse("accounts:login")

    # When
    response = client.post(
        url,
        data={"username": user.username, "password": "valid_pass123"},
    )

    # Then
    assert response.status_code == 302
    assert response.url == reverse("contacts:create")


@pytest.mark.django_db
def test_logout_logs_out_user_and_redirects_to_login(client):
    # Given
    user = User.objects.create_user(username="logout_user", password="valid_pass123")
    client.force_login(user)
    url = reverse("accounts:logout")

    # When
    response = client.get(url)

    # Then
    assert response.status_code == 302
    assert response.url == reverse("accounts:login")
