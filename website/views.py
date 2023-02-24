from django.shortcuts import render
from django.views import View
from website.models import Donation, Institution, Category
from django.db.models import Sum


class LandingPage(View):
    def get(self, request):
        institution = Institution.objects.all()
        categories = Category.objects.all()
        institution_quantity = Donation.objects.values_list('quantity', flat=True)
        total_quantity = Donation.objects.aggregate(total=Sum('quantity'))['total']
        return render(request, "website/index.html", context={
            "institution": institution,
            "categories": categories,
            "institution_quantity": institution_quantity,
            "total_quantity": total_quantity,
        })

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