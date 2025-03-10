
from django.urls import path

from . import views

urlpatterns = [
    path('cats/<int:cat_id>/', views.catg, name='cats_id'),
    path('product/<int:product_id>/', views.show_product, name='product'),
    path('c/<slug:category_slug>/', views.show_category, name='category'),
    path('shop/<int:seller_id>/', views.show_shop, name='shop'),
    path('addprod/', views.addprod, name='addprod'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('cart-add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart-delete/<int:cart_id>/', views.cart_delete, name='cart_delete'),
    path('cart-decr/<int:cart_id>/', views.cart_decr, name='cart_decr'),
    path('cart/', views.show_cart, name='cart'),
    path('create_order/', views.create_order, name='create_order'),
    path('pay_order/', views.pay_order, name='pay_order'),
    path('cart-decr-index/<int:product_id>/', views.cart_decr_in_index, name='cart_decr_in_index'),
    path('add-fav/<int:product_id>/', views.add_fav, name='add_fav'),
    path('rem-fav/<int:product_id>/', views.rem_fav, name='rem_fav'),
    path('favorites/', views.show_favorites, name='favorites'),
    path('cart-add-ajax/', views.cart_add_ajax, name='cart_add_ajax'),
    # path('cart-add-ajax1/', views.cart_add_ajax, name='cart_add_ajax1'),
    path('cart-decr-index_ajax/', views.cart_decr_in_index_ajax, name='cart_decr_in_index_ajax'),
    path('orders/', views.show_orders, name='orders'),
    path('orders_shop/', views.show_orders_for_shop, name='orders_shop'),
    path('', views.index, name='home'),
    path('s/', views.search, name='search'),
    path('rem_review/<int:rev_id>/', views.rem_review, name='rem_review'),
    path('edit_order/<int:order_id>/', views.edit_order, name='edit_order'),

]
