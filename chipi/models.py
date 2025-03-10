import os

from django.db import models
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from users.models import User, Buyer


# from users.models import User
# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    count = models.PositiveIntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='products', blank=True)
    prodcategory = models.ForeignKey('ProdCategory', on_delete=models.PROTECT, related_name='products', null=True)
    shop = models.ForeignKey('Shop', on_delete=models.PROTECT, related_name='products')
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    logo_image = models.ImageField(upload_to='logos/')

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_id': self.pk})

    def save(self, *args, **kwargs):
        try:
            this = Product.objects.get(id=self.id)
            if this.logo_image != self.logo_image:
                if os.path.isfile(this.logo_image.path):
                    os.remove(this.logo_image.path)
        except:
            pass

        super(Product, self).save(*args, **kwargs)

    # def __str__(self):
    #     return self.title

    class Meta:
        ordering = ["pk"]


class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='photos/')


class ProdCategory(MPTTModel):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='Родительская категория')
    slug = models.SlugField(max_length=63, unique=True, db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = [['parent', 'slug']]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    # def get_absolute_url(self):
    #     return reverse('post-by-category', args=[str(self.slug)])

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name



class Shop(models.Model):
    '''- id
        - seller_id
        - name
        - (Rating)
        - (Sklad address)'''
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='shop', null=True)
    name = models.CharField(max_length=63, db_index=True)
    email = models.EmailField(blank=True, unique=True, null=True)
    phone = models.CharField(blank=True, null=True, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop', kwargs={'seller_id': self.pk})

    class Meta:
        ordering = ["pk"]


class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')
    # from_user = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    score = models.PositiveIntegerField()
    image = models.ImageField(upload_to='reviews/', blank=True)


class Cart(models.Model):
    user = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='cart')
    count = models.PositiveIntegerField(default=1)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    def sum(self):
        return self.count * self.product.price


class Favorite(models.Model):
    user = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='favorite')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='favorite')
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-time_created"]


class Order(models.Model):
    class Status(models.IntegerChoices):
        CREATED = 0, 'Создан'
        PAID_FOR = 1, 'Оплачен'
        ASSEMBLING = 2, 'В сборке'
        TRANSIT = 3, 'В пути'
        WAITING = 4, 'Ожидает выдачи'
        DELIVERED = 5, 'Доставлен'
    '''+ address'''
    user = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='orders')
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, related_name='orders', null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='orders', null=True)
    count = models.PositiveIntegerField()
    price = models.PositiveBigIntegerField()
    time_created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=Status.choices, default=Status.CREATED)
    title = models.CharField(max_length=255)
    track = models.CharField(blank=True)

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
