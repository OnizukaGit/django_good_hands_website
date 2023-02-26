from django.shortcuts import render
from django.views import View
from website.models import Donation, Institution, Category
from django.db.models import Sum
from django.core.paginator import Paginator



class LandingPage(View):
    def get(self, request):
        institution = Institution.objects.filter(type=0)
        organizations = Institution.objects.filter(type=1)
        local = Institution.objects.filter(type=2)
        categories = Category.objects.all()
        institution_quantity = Donation.objects.values_list('quantity', flat=True)
        total_quantity = Donation.objects.aggregate(total=Sum('quantity'))['total']
        p = Paginator(Institution.objects.all(), 2)
        page = request.GET.get('page')
        institution_page = p.get_page(page)
        return render(request, "website/index.html", context={
            "institution": institution,
            "organizations": organizations,
            "local": local,
            "categories": categories,
            "institution_quantity": institution_quantity,
            "total_quantity": total_quantity,
            "institution_page": institution_page,
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