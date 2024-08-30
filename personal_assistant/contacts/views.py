from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from .models import Contact
from .forms import ContactForm


def contact_list(request):
    birthday = request.GET.get('birthday')
    contacts = Contact.objects.filter(user=request.user)

    if birthday:
        contacts = contacts.filter(birthday=birthday)

    return render(request, 'contacts/contact_list.html', {'contacts': contacts})


def contact_search(request):
    query = request.GET.get('q')
    contacts = Contact.objects.filter(user=request.user)

    if query:
        contacts = contacts.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(email__icontains=query)
        )

    return render(request, 'contacts/contact_list.html', {'contacts': contacts})


def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contacts/contact_edit.html', {'form': form})


def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    if request.method == 'POST':
        contact.delete()
        return redirect('contact_list')
    return render(request, 'contacts/contact_delete_confirm.html', {'contact': contact})
