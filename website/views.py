from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, RedirectView
from website.models import Donation, Institution, Category
from django.db.models import Sum
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from website.forms import RegisterForm, LoginForm
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from rest_framework import generics
from .serializers import DonationSerializer, CategorySerializer, InstitutionSerializer


class LandingPage(View):
    def get(self, request):
        institution = Institution.objects.filter(type=0)
        organizations = Institution.objects.filter(type=1)
        local = Institution.objects.filter(type=2)
        categories = Category.objects.all()
        institution_quantity = Donation.objects.values_list('quantity', flat=True)
        total_quantity = Donation.objects.aggregate(total=Sum('quantity'))['total']
        one = Paginator(Institution.objects.filter(type="0").order_by('name'), 2)
        two = Paginator(Institution.objects.filter(type="1").order_by('name'), 2)
        three = Paginator(Institution.objects.filter(type="2").order_by('name'), 2)
        page = request.GET.get('page')
        institution_page_one = one.get_page(page)
        institution_page_two = two.get_page(page)
        institution_page_three = three.get_page(page)
        return render(request, "website/index.html", context={
            "institution": institution,
            "organizations": organizations,
            "local": local,
            "categories": categories,
            "institution_quantity": institution_quantity,
            "total_quantity": total_quantity,
            "institution_page_one": institution_page_one,
            "institution_page_two" : institution_page_two,
            "institution_page_three" : institution_page_three,
        })


class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class InstitutionView(generics.ListCreateAPIView):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


class DonationView(generics.ListCreateAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer


class AddDonation(View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, "website/form.html", context={"categories": categories, "institutions": institutions})


class FormConfirmation(View):
    def get(self, request):
        return render(request, "website/form-confirmation.html")


class Login(LoginView):
    redirect_authenticated_user = True
    template_name = 'website/login.html'
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class Logout(RedirectView):
    url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(Logout, self).get(request, *args, **kwargs)


class Register(CreateView):
    template_name = "website/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        response = super().form_valid(form)
        cd = form.cleaned_data
        self.object.set_password(cd['password1'])
        self.object.save()
        return response




