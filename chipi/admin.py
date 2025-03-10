from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Product, Review, Category, Shop, Cart, ProdCategory, Order


# Register your models here.


class CategoryAdmin(MPTTModelAdmin):
    prepopulated_fields = {"slug": ("name",)}



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'prodcategory', 'shop')
    search_fields = ['title', 'prodcategory__name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'count', 'user', 'status')
    # search_fields = ['title', 'prodcategory__name']

admin.site.register(ProdCategory, CategoryAdmin)

# admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Shop)
admin.site.register(Review)
admin.site.register(Cart)


