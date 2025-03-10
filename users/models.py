from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    is_buyer = models.BooleanField(default=False)
    is_shop = models.BooleanField(default=False)


class Buyer(models.Model):
    class Age(models.IntegerChoices):
        MALE = 0, 'Мужской'
        FEMALE = 1, 'Женский'

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='buyer')
    first_name = models.CharField(max_length=63, blank=True)
    middle_name = models.CharField(max_length=63, blank=True)
    last_name = models.CharField(max_length=63, blank=True)
    email = models.EmailField(blank=True, unique=True, null=True)
    phone = models.CharField(blank=True, null=True, unique=True)
    sex = models.BooleanField(choices=Age.choices, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    correct_address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='buyer', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Address(models.Model):
    user = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='address')
    first_name = models.CharField(max_length=63)
    middle_name = models.CharField(max_length=63, blank=True)
    last_name = models.CharField(max_length=63)
    email = models.EmailField()
    phone = models.CharField()
    country = models.CharField()
    region = models.CharField()
    city = models.CharField()
    index = models.CharField()
    addr = models.CharField()

