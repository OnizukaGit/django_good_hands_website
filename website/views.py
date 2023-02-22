from django.shortcuts import render
from django.views import View
from website.models import Donation
from django.db.models import Sum


class LandingPage(View):
    def get(self, request):
        institution = Donation.objects.values_list('quantity', flat=True)
        total_quantity = Donation.objects.aggregate(total=Sum('quantity'))['total']
        return render(request, "website/index.html", context={"institution": institution,
                                                              "total_quantity": total_quantity})


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