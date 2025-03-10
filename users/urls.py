from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    # path('profile/', views.ProfileUser.as_view(), name='profile'),
    path('profile/', views.profile, name='profile'),
    path('password-change/', views.UserPasswordChange.as_view(), name='password_change'),
    path('password-change/done', PasswordChangeDoneView.as_view(template_name='user/password_change_done.html'),
         name='password_change_done'),
    path('shop-register/', views.RegisterShop.as_view(), name='shop_register'),
    path('edit_shop/', views.edit_shop, name='edit_shop'),
    path('address/', views.address, name='address')
]
