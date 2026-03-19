import pytest
from contacts.models import Contact


@pytest.mark.django_db
def test_contact_str_returns_subject():
    # Given
    contact = Contact.objects.create(
        subject="Subject line",
        email="user@example.com",
        message="Hello",
        cc_myself=False,
    )

    # When
    result = str(contact)

    # Then
    assert result == "Subject line"
