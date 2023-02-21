from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=64)


class Institution(models.Model):
    INSTITUTION_TYPES = [
        ("Fundacja", 'Fundacja'),
        ("Organizacja porządkowa", 'Organizacja pozarządowa'),
        ("Zbiórka lokalna", 'Zbiórka lokalna'),
    ]
    name = models.CharField(max_length=64)
    description = models.TextField()
    type = models.CharField(max_length=64, choices=INSTITUTION_TYPES, default="Fundacja")
    categories = models.ManyToManyField(Category)


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

