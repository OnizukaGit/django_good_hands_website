from django.contrib import messages
from django.views import View
from django.views.generic import CreateView, RedirectView, ListView, UpdateView
from website.models import Donation, Institution, Category
from django.db.models import Sum
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from website.forms import RegisterForm, LoginForm, DonationForm
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from rest_framework import generics
from .serializers import DonationSerializer, CategorySerializer, InstitutionSerializer
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


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
            "institution_page_two": institution_page_two,
            "institution_page_three": institution_page_three,
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


class UserPanel(ListView):
    template_name = 'website/my_profile.html'
    model = User
    context_object_name = "users"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(username=self.request.user.username)


class AddDonation(CreateView):
    template_name = "website/form.html"
    success_url = reverse_lazy('form-confirmation')
    form_class = DonationForm


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


class ListUsers(ListView):
    template_name = 'website/list_users.html'
    model = User
    context_object_name = 'users'
    ordering = ['id']

    def test_func(self):
        return self.request.user.is_superuser


class UpdateUsers(UpdateView):
    template_name = 'website/update_users.html'
    model = User
    fields = ['username', 'first_name', 'email', 'is_superuser']
    success_url = reverse_lazy('list-users')

    def test_func(self):
        return self.request.user.is_superuser


class PasswordReset(View):
    def get(self, request):
        password_reset_form = PasswordResetForm()
        return render(request=request, template_name="website/reset_password.html",
                      context={"password_reset_form": password_reset_form})

    def post(self, request):
        if request.method == "POST":
            password_reset_form = PasswordResetForm(request.POST)
            if password_reset_form.is_valid():
                data = password_reset_form.cleaned_data['email']
                associated_users = User.objects.filter(Q(email=data))
                if associated_users.exists():
                    for user in associated_users:
                        subject = "Resetowanie Hasla"
                        email_template_name = "website/password_reset_email.txt"
                        c = {
                            "email": user.email,
                            'domain': '127.0.0.1:8000',
                            'site_name': 'website',
                            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                            'user_email': user.email,
                        }
                        email = render_to_string(email_template_name, c)
                        try:
                            send_mail(subject, email, "resethasla@admin.com", [user.email], fail_silently=False)
                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')
                        return redirect("password_reset_done")
                messages.error(request, 'An invalid email has been entered.')
        return render(request=request, template_name="website/password_reset_done.html")

