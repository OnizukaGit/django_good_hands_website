from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm


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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nazwa użytkownika", max_length=254)
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)