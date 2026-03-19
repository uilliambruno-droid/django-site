import pytest
from contacts.forms import ContactForm, NameForm
from contacts.models import Contact


def test_name_form_is_valid_with_valid_data():
    # Given
    payload = {"your_name": "Uilliam"}

    # When
    form = NameForm(data=payload)

    # Then
    assert form.is_valid()
    assert form.cleaned_data["your_name"] == "Uilliam"


def test_name_form_is_invalid_when_name_is_missing():
    # Given
    payload = {}

    # When
    form = NameForm(data=payload)

    # Then
    assert not form.is_valid()
    assert "your_name" in form.errors


def test_name_form_is_invalid_when_name_exceeds_max_length():
    # Given
    payload = {"your_name": "a" * 101}

    # When
    form = NameForm(data=payload)

    # Then
    assert not form.is_valid()
    assert "your_name" in form.errors


def test_contact_form_is_valid_with_complete_data():
    # Given
    payload = {
        "subject": "New contact",
        "email": "user@example.com",
        "message": "Hello there",
        "cc_myself": True,
    }

    # When
    form = ContactForm(data=payload)

    # Then
    assert form.is_valid()


def test_contact_form_is_invalid_with_bad_email():
    # Given
    payload = {
        "subject": "New contact",
        "email": "invalid-email",
        "message": "Hello there",
        "cc_myself": False,
    }

    # When
    form = ContactForm(data=payload)

    # Then
    assert not form.is_valid()
    assert "email" in form.errors


def test_contact_form_is_invalid_when_required_fields_are_missing():
    # Given
    payload = {"cc_myself": False}

    # When
    form = ContactForm(data=payload)

    # Then
    assert not form.is_valid()
    assert "subject" in form.errors
    assert "email" in form.errors
    assert "message" in form.errors


@pytest.mark.django_db
def test_contact_form_save_persists_contact_model():
    # Given
    payload = {
        "subject": "Saved contact",
        "email": "save@example.com",
        "message": "Persistent message",
        "cc_myself": True,
    }
    form = ContactForm(data=payload)

    # When
    contact = form.save() if form.is_valid() else None

    # Then
    assert contact is not None
    assert Contact.objects.filter(id=contact.id).exists()
    assert contact.subject == "Saved contact"
