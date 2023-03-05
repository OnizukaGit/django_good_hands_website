from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Institution(models.Model):
    FUNDACJA = 0
    ORGANIZACJA_POZARZADOWA = 1
    ZBIORKA_LOKALNA = 2

    ORGANIZATIONS = (
        (FUNDACJA, 'fundacja'),
        (ORGANIZACJA_POZARZADOWA, 'organizacja pozarządowa'),
        (ZBIORKA_LOKALNA, 'zbiórka lokalna'),
    )

    name = models.CharField(max_length=128)
    description = models.TextField(null=True)
    type = models.SmallIntegerField(choices=ORGANIZATIONS, default=FUNDACJA)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=64)
    phone_regex = RegexValidator(
        regex=r'^\d{9,}$',
        message='Numer telefonu musi składać się z co najmniej 9 cyfr'
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=12)
    city = models.CharField(max_length=30)
    zip_regex = RegexValidator(
        regex=r'^\d{2}-\d{3}$',
        message='Kod pocztowy musi mieć format xx-xxx'
    )
    zip_code = models.CharField(max_length=6, validators=[zip_regex])
    pick_up_date = models.DateTimeField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Users(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    groups = models.ManyToManyField("auth.Group", blank=True, related_name="user_groups")
    user_permissions = models.ManyToManyField("auth.Permission", blank=True, related_name="user_permissions")