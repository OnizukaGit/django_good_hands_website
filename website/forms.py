from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class RegisterForm(forms.ModelForm):
    pass1 = forms.CharField(label="Hasło", widget=forms.PasswordInput)
    pass2 = forms.CharField(label="Powtórz hasło", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
        )
        help_texts = {
            'username': 'Tym będziesz się logował',
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ta nazwa użytkownika już istnieje")
        return username

    def clean(self):
        cd = super().clean()
        pass1 = cd.get('pass1')
        pass2 = cd.get('pass2')
        if len(pass1) < 4:
            raise forms.ValidationError('Hasło musi mieć więcej niż 4 litery!')
        if pass1 != pass2:
            raise forms.ValidationError('Hasło musi być takie same')


class LoginForm(forms.Form):
    username = forms.CharField(label="Nazwa użytkownika")
    password1 = forms.CharField(label="Hasło", widget=forms.PasswordInput)

    def clean(self):
        cd = super().clean()

        username = cd.get('username')
        password1 = cd.get('password1')
        user = authenticate(username=username, password=password1)

        if user is None:
            raise forms.ValidationError("Złe podane hasło lub login")