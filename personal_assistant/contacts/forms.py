from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'birthday']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if len(phone_number) == 10:
            # Додати код країни України, якщо номер має 10 цифр
            phone_number = '+380' + phone_number
        elif len(phone_number) == 11 and phone_number.startswith('0'):
            # Замінити 0 на +380, якщо номер починається з 0
            phone_number = '+380' + phone_number[1:]
        elif len(phone_number) == 12 and phone_number.startswith('380'):
            # Додати "+" якщо номер починається з 380
            phone_number = '+' + phone_number
        elif len(phone_number) == 13 and phone_number.startswith('+380'):
            # Якщо номер вже в правильному форматі, залишити його
            pass
        else:
            raise forms.ValidationError("Невірний формат номера телефону. Введіть номер у форматі +380XXXXXXXXX.")
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not forms.EmailField().clean(email):
            raise forms.ValidationError("Невірний формат email.")
        return email