from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm, RegisterShopForm, \
    ProfileUser2Form, ProfileShopForm, AddressForm

from django.contrib.auth.decorators import login_required

from users.models import Address


# from django.contrib.auth import login as auth_login

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    # extra_context = {'title' 'NYA'}
    # def get_success_url(self):
    #     return reverse_lazy('home')

    # def form_valid(self, form):
    #     cd = form.cleaned_data
    #     """Security check complete. Log the user in."""
    #     user = authenticate(self.request, username=cd['username'], password=cd['password'], is_buyer=True)
    #     if user is not None:
    #         # Логика при успешной аутентификации
    #         return super().form_valid(form)
    #     else:
    #         # Логика при неудачной аутентификации
    #         return super().form_invalid(form)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

# def register(request):
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             return render(request, 'users/register_done.html')
#     else:
#         form = RegisterUserForm
#     return render(request, 'users/register.html', {'form': form})




# def login_user(request):
#     if request.method == 'POST':
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user and user.is_active:
#                 login(request, user)
#                 return redirect('home')
#     else:
#         form = LoginUserForm()
#     return render(request, 'users/login.html', {'form': form})
#     # return HttpResponse('login')


def logout_user(request):
    logout(request)
    return redirect('users:login')


# class ProfileUser(LoginRequiredMixin, UpdateView):
#     model = get_user_model()
#     form_class = ProfileUserForm
#     template_name = 'users/profile.html'
#
#     def get_success_url(self):
#         return reverse_lazy('users:profile')
#
#     def get_object(self, queryset=None):
#         return self.request.user

login_required
def profile(request):
    user = request.user
    if not user.is_buyer:
        return HttpResponseNotFound('<h1>Страница не найдена</h1>')

    form = ProfileUserForm(instance=user)
    form2 = ProfileUser2Form(instance=user.buyer)

    if request.method == 'POST':
        form = ProfileUserForm(request.POST, instance=user)
        form2 = ProfileUser2Form(request.POST, instance=user.buyer)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return redirect(reverse_lazy('users:profile'))
    return render(request, 'users/profile.html', {'form': form, 'form2': form2})


def edit_shop(request):
    user = request.user
    if not user.is_shop:
        return HttpResponseNotFound('<h1>Страница не найдена</h1>')

    form = ProfileUserForm(instance=user)
    form2 = ProfileShopForm(instance=user.shop)

    if request.method == 'POST':
        form = ProfileUserForm(request.POST, instance=user)
        form2 = ProfileShopForm(request.POST, instance=user.shop)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return redirect(reverse_lazy('users:edit_shop'))
    return render(request, 'users/edit_shop.html', {'form': form, 'form2': form2})

# def profile_a(request):
#     if request.method == 'POST':
#         form = ProfileUserForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             try:
#                 # Product.objects.create(**form.cleaned_data)
#                 print('a')
#                 return redirect('home')
#             except:
#                 form.add_error(None, 'Ошибка добавления хз')
#
#     else:
#         form = ProfileUserForm()
#     return render(request, 'users/profile.html', {'form': form})




class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"


class RegisterShop(CreateView):
    form_class = RegisterShopForm
    template_name = 'users/shop_register.html'
    success_url = reverse_lazy('home')


def address(request):
    user = request.user
    if not user.is_authenticated:
        return redirect(reverse_lazy('users:login'))
    if not user.is_buyer:
        return HttpResponseNotFound('<h1>Страница не найдена</h1>')
    indata = {
        'phone': user.buyer.phone,
        'email': user.buyer.email,
        'last_name': user.buyer.last_name,
        'first_name': user.buyer.first_name,
        'middle_name': user.buyer.middle_name,
    }
    if user.buyer.correct_address:
        form = AddressForm(instance=user.buyer.correct_address)
    else:
        form = AddressForm(initial=indata)

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            try:
                if not user.buyer.correct_address:
                    a = Address.objects.create(**form.cleaned_data, user=user.buyer)
                    u = user.buyer
                    u.correct_address = a
                    u.save()
                else:
                    adr = user.buyer.correct_address.id
                    Address.objects.filter(pk=adr).update(**form.cleaned_data)
                return redirect('users:address')
            except:
                form.add_error(None, 'Ошибка добавления хз')

            return redirect(reverse_lazy('users:address'))
    return render(request, 'users/address.html', {'form': form})
