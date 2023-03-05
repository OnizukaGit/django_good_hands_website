from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForms(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Hasło")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Powtórz hasło")

    class Meta:
        model = User
        fields = [
            "username", "first_name", "last_name", "email"
        ]

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Ten email jest już zarejestrowany.")
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Hasła nie są identyczne.")
        return password2




