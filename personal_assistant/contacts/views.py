from datetime import timedelta

from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.template.defaulttags import now

from .models import Contact
from .forms import ContactForm
import logging

# Налаштування базового логування
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def contact_list(request):
    birthday = request.GET.get('birthday')
    contacts = Contact.objects.filter(user=request.user)

    if birthday:
        contacts = contacts.filter(birthday=birthday)

    return render(request, 'contacts/contact_list.html', {'contacts': contacts})


def contact_search(request):
    query = request.GET.get('q', '')  # Пошуковий запит для імені, телефону чи email
    birthday = request.GET.get('birthday', '')
    days_until_birthday = request.GET.get('days_until_birthday', '')

    # Фільтрація контактів по користувачу
    contacts = Contact.objects.filter(user=request.user)
    logger.debug(f"Initial contacts count: {contacts.count()}")

    # Створення базового Q об'єкта для фільтрації
    filters = Q()

    # Пошук за ім'ям, телефоном або email
    if query:
        filters &= (
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(email__icontains=query)
        )
        logger.debug(f"Added query filter: '{query}'")

    # Фільтрація за точною датою народження
    if birthday:
        try:
            birthday_date = now().date().replace(year=int(birthday))
            filters &= Q(birthday=birthday_date)
            logger.debug(f"Added birthday filter: '{birthday}'")
        except ValueError:
            logger.error(f"Invalid birthday value: {birthday}")

    # Фільтрація за кількістю днів до дня народження
    if days_until_birthday:
        try:
            days_until_birthday = int(days_until_birthday)
            today = now().date()
            target_date = today + timedelta(days=days_until_birthday)

            # Фільтрація контактів за місяцем і днем
            filters &= Q(birthday__month=target_date.month, birthday__day=target_date.day)
            logger.debug(f"Added days_until_birthday filter: '{days_until_birthday}'")
        except ValueError:
            logger.error(f"Invalid days_until_birthday value: {days_until_birthday}")

    # Застосування всіх фільтрів до контактів
    contacts = contacts.filter(filters)
    logger.debug(f"Final contacts count after all filters: {contacts.count()}")

    return render(request, 'contacts/contact_list.html', {'contacts': contacts})


def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    if request.method == 'POST':
        contact.delete()
        return redirect('contact_list')
    return render(request, 'contacts/contact_delete_confirm.html', {'contact': contact})

def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('contact_list')
    else:
        form = ContactForm()
    return render(request, 'contacts/contact_create.html', {'form': form})
