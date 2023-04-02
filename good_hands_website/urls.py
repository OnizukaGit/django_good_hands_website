"""good_hands_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from website.views import LandingPage, AddDonation, FormConfirmation, Login, Register,\
                            Logout, CategoriesView, DonationView, InstitutionView, UserPanel,\
                            ListUsers, UpdateUsers, ResetPassword, PasswordResetDone, PasswordResetConfirm, \
                            PasswordResetComplete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPage.as_view(), name="index"),
    path('form/', AddDonation.as_view(), name="form"),
    path('form-confirmation', FormConfirmation.as_view(), name="form-confirmation"),
    path('profile/', UserPanel.as_view(), name="user-panel"),

    path('register/', Register.as_view(), name="register"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),

    path('reset-password/', ResetPassword.as_view(), name='reset_password'),
    path('reset-password-sent/', PasswordResetDone.as_view(), name="password_reset_done"),
    path('reset/<uid64>/<token>/', PasswordResetConfirm.as_view(), name="password_reset_confirm"),
    path('reset-password-complete/,', PasswordResetComplete.as_view(), name="password_reset_complete"),

    path('list-users/', ListUsers.as_view(), name="list-users"),
    path('update-user/<int:pk>', UpdateUsers.as_view(), name='update-user'),

    path('categories/<int:pk>', CategoriesView.as_view(), name="category-serializer"),
    path('donation/<int:pk>', DonationView.as_view(), name="category-serializer"),
    path('institution/<int:pk>', InstitutionView.as_view(), name="category-serializer"),
]
