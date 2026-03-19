from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ContactForm, NameForm


@permission_required("contacts.add_contact", raise_exception=True)
def create(request):

    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse("contacts:thanks", args=(form.cleaned_data["subject"],))
            )
    else:
        form = ContactForm()
    return render(request, "contacts/create.html", {"form": form})


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data["your_name"]
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect(reverse("contacts:thanks", args=(name,)))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, "contacts/name.html", {"form": form})


def thanks(request, name):
    return HttpResponse(f"Thanks for submitting your name, {name}!")
