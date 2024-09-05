from datetime import timedelta

from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.template.defaulttags import now
from datetime import date

from .models import Contact
from .forms import ContactForm
import logging

# Налаштування базового логування
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def contact_list(request):
    search_name = request.GET.get(
        "name"
    )  # Пошуковий запит для імені, телефону чи email
    search_birth_date = request.GET.get("birth_date")  # Пошуковий запит за др
    search_days_to_birthday = request.GET.get(
        "days_to_birthday"
    )  # Пошуковий запит за кількістю днів до др
    contacts = Contact.objects.filter(user=request.user)

    # Пошук за ім'ям, телефоном або email
    if search_name:
        contacts = contacts.filter(first_name__icontains=search_name) | contacts.filter(
            last_name__icontains=search_name
        )

    # Фільтрація за точною датою народження
    if search_birth_date:
        contacts = contacts.filter(birthday=search_birth_date)

    # Фільтрація за кількістю днів до дня народження
    if search_days_to_birthday:
        search_days_to_birthday = int(search_days_to_birthday)
        contacts = [
            contact
            for contact in contacts
            if contact.days_until_birthday() == search_days_to_birthday
        ]

    return render(request, "contacts/contact_list.html", {"contacts": contacts})


def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    if request.method == "POST":
        contact.delete()
        return redirect("contact_list")
    return render(request, "contacts/contact_delete_confirm.html", {"contact": contact})


def contact_create(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect("contact_list")
    else:
        form = ContactForm()
    return render(request, "contacts/contact_create.html", {"form": form})


def contact_edit(request, pk):  # Додайте pk у функцію
    contact = get_object_or_404(Contact, pk=pk)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_list')  # Ваша URL назва для списку контактів
    else:
        form = ContactForm(instance=contact)

    return render(request, 'contacts/contact_edit.html', {'form': form})
