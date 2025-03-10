import pytest
import django

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market.settings')
django.setup()
from django.contrib.auth.models import AnonymousUser
from django.test import Client
from users.models import User, Buyer
from .models import Product, Cart


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def buyer(db, user):
    return Buyer.objects.create(user=user)


@pytest.fixture
def product(db):
    return Product.objects.create(title="Test Product", price=100, count=10)


@pytest.fixture
def cart(db, buyer, product):
    return Cart.objects.create(user=buyer, product=product, count=1)


def test_cart_add(client, user, product):
    client.login(username="testuser", password="testpass")
    response = client.post(f"/cart/add/{product.id}/")
    assert response.status_code == 302


def test_cart_add_unauthenticated(client, product):
    response = client.post(f"/cart/add/{product.id}/")
    assert response.status_code == 302  # Должен редиректить на логин
