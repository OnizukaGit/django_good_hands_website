from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView, RedirectView, ListView, DeleteView, UpdateView, DetailView
from website.models import Donation, Institution, Category
from django.db.models import Sum
from django.core.paginator import Paginator
from django.urls import reverse_lazy, reverse
from website.forms import RegisterForm, LoginForm, DonationForm, ResetPasswordForm
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from rest_framework import generics
from .serializers import DonationSerializer, CategorySerializer, InstitutionSerializer
from django.contrib.auth.models import User


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


class ResetPassword(PasswordResetView):
    template_name = 'website/reset_password.html'
    email_template_name = 'website/password_reset_email.html' # nowy szablon e-mail
    success_url = reverse_lazy('password_reset_done') # musisz zdefiniować URL do success_url

    def send_mail(self, email, html_content, subject):
        msg = EmailMultiAlternatives(
            subject=subject, from_email=settings.EMAIL_FROM, to=[email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        if user is not None:
            current_site = get_current_site(self.request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = reverse(
                'password_reset_confirm', args=[uid, token]
            )
            reset_url = f"https://{current_site.domain}{reset_url}"
            context = {
                'user': user,
                'reset_url': reset_url,
                'current_site': current_site,
            }
            subject = 'Resetuj hasło'
            body = loader.render_to_string(
                self.email_template_name, context=context
            )
            self.send_mail(email, body, subject)
        return super().form_valid(form)


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'website/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'website/password_reset_complete.html'


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'website/password_reset_done.html'
