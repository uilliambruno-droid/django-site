import pytest
from contacts.models import Contact
from django.contrib.auth.models import Permission, User
from django.urls import reverse


@pytest.mark.django_db
def test_get_name_get_renders_form(client):
    # Given
    url = reverse("contacts:get_name")

    # When
    response = client.get(url)

    # Then
    assert response.status_code == 200
    assert "Submit" in response.content.decode()


@pytest.mark.django_db
def test_get_name_post_valid_redirects_to_thanks(client):
    # Given
    url = reverse("contacts:get_name")

    # When
    response = client.post(url, data={"your_name": "Uilliam"})

    # Then
    assert response.status_code == 302
    assert response.url == reverse("contacts:thanks", args=["Uilliam"])


@pytest.mark.django_db
def test_get_name_post_invalid_redisplays_form(client):
    # Given
    url = reverse("contacts:get_name")

    # When
    response = client.post(url, data={})

    # Then
    assert response.status_code == 200
    assert "Submit" in response.content.decode()


@pytest.mark.django_db
def test_thanks_returns_confirmation_message(client):
    # Given
    url = reverse("contacts:thanks", args=["Uilliam"])

    # When
    response = client.get(url)

    # Then
    assert response.status_code == 200
    assert "Thanks for submitting your name, Uilliam!" in response.content.decode()


@pytest.mark.django_db
def test_create_returns_403_for_anonymous_user(client):
    # Given
    url = reverse("contacts:create")

    # When
    response = client.get(url)

    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_create_returns_403_for_authenticated_user_without_permission(client):
    # Given
    user = User.objects.create_user(username="no_perm", password="secret123")
    client.force_login(user)
    url = reverse("contacts:create")

    # When
    response = client.get(url)

    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_create_get_with_permission_renders_form(client):
    # Given
    user = User.objects.create_user(username="with_perm", password="secret123")
    add_contact_permission = Permission.objects.get(codename="add_contact")
    user.user_permissions.add(add_contact_permission)
    client.force_login(user)
    url = reverse("contacts:create")

    # When
    response = client.get(url)

    # Then
    assert response.status_code == 200
    assert "Submit" in response.content.decode()


@pytest.mark.django_db
def test_create_post_with_permission_creates_contact_and_redirects(client):
    # Given
    user = User.objects.create_user(username="with_perm", password="secret123")
    add_contact_permission = Permission.objects.get(codename="add_contact")
    user.user_permissions.add(add_contact_permission)
    client.force_login(user)

    url = reverse("contacts:create")
    payload = {
        "subject": "New contact",
        "email": "user@example.com",
        "message": "Hello there",
        "cc_myself": True,
    }

    # When
    response = client.post(url, data=payload)

    # Then
    assert response.status_code == 302
    assert response.url == reverse("contacts:thanks", args=["New contact"])
    assert Contact.objects.filter(
        subject="New contact", email="user@example.com"
    ).exists()
