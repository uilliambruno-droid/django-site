from django import forms

from .models import Contact


class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)


class ContactForm(forms.ModelForm):
    subject = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    cc_myself = forms.BooleanField(required=False)

    class Meta:
        model = Contact
        fields = ["subject", "email", "message", "cc_myself"]
