from captcha.fields import CaptchaField, CaptchaTextInput
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from website.models import Donation

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=64)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Hasło")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Powtórz hasło")

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]
        labels = {
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'email': 'Email',

        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ten mail jest już w bazie")
        return email


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254)
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': "Nieprawidłowy adres e-mail"
    }

    captcha = CaptchaField()


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = [
            'quantity',
            'categories',
            'institution',
            'address',
            'phone_number',
            'city',
            'zip_code',
            'pick_up_date',
            'pick_up_time',
            'pick_up_comment',
        ]
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
            'pick_up_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'pick_up_time': forms.TimeInput(attrs={'type': 'time'}),
        }
