from django.shortcuts import render
from django.views import View


class LandingPage(View):
    def get(self, request):
        return render(request, "website/index.html")


class AddDonation(View):
    def get(self, request):
        return render(request, "website/form.html")


class FormConfirmation(View):
    def get(self, request):
        return render(request, "website/form-confirmation.html")


class Login(View):
    def get(self, request):
        return render(request, "website/login.html")


class Register(View):
    def get(self, request):
        return render(request, "website/register.html")