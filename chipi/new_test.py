from django.urls import reverse
import pytest
import django

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market.settings')
django.setup()
from django.contrib.auth.models import AnonymousUser
from django.test import Client
from users.models import Address, User, Buyer
from .models import Order, Product, Cart


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
    assert response.status_code == 302  


def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="buyer", password="testpass")
        self.user.is_buyer = True
        self.user.save()

        self.product = Product.objects.create(title="Test Product", price=100, count=5)
        self.cart = Cart.objects.create(user=self.user.buyer, product=self.product, count=2)
        
        self.address = Address.objects.create(
            user=self.user.buyer,
            first_name="Vika",
            last_name="Kaz",
            phone="79149111111",
            email="test@example.com",
            country="Russia",
            region="Moscow region",
            city="Moscow",
            addr="123 Test Street",
            index="123412"
        )
        self.user.buyer.correct_address = self.address
        self.user.buyer.save()

        self.client.login(username="buyer", password="testpass")


def test_pay_order(self):
    response = self.client.post(reverse("pay_order"), {"payment_method": "card"})
    self.assertRedirects(response, reverse("orders")) 
    self.assertFalse(Cart.objects.filter(user=self.user.buyer).exists())  
    self.assertEqual(Order.objects.count(), 1)  


def test_pay_order_with_insufficient_stock(self):
    self.product.count = 1  
    self.product.save()
    response = self.client.post(reverse("pay_order"), {"payment_method": "card"})
    self.assertRedirects(response, reverse("pay_order"))  
    self.assertContains(response, "Количество доступных товаров изменилось")
