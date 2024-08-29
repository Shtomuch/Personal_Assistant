from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'birthday']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit() or len(phone_number) not in [10, 11, 15]:
            raise forms.ValidationError("Невірний формат номера телефону.")
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not forms.EmailField().clean(email):
            raise forms.ValidationError("Невірний формат email.")
        return email