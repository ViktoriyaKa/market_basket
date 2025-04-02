import os

from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy  # type: ignore
from django.forms import modelformset_factory

from users.forms import AddressForm, PaymentTestForm
from users.models import Address
from .forms import AddProdForm, ImageForm, ReviewForm, EditOrderForm
from .models import (
    Product,
    Category,
    Shop,
    Cart,
    Favorite,
    Order,
    ProductImage,
    ProdCategory,
    Review,
)
from django.db.models import Avg, Count, Q, Sum, Min


# Create your views here.


def get_products(user, search_query=None):
    filters = {}
    if search_query:
        filters["title__icontains"] = search_query

    products = (
        Product.objects.filter(**filters)
        .annotate(mark=Avg("reviews__score"))
        .select_related("shop")
    )

    if user.is_authenticated and user.is_buyer:
        products = products.annotate(
            count_in_cart=Min("cart__count", filter=Q(cart__user=user.buyer))
        )

    return products


@login_required
def index(request):
    search_query = request.GET.get("q", "")
    products = get_products(request.user, search_query)
    fav_prod = (
        Product.objects.filter(favorite__user=request.user.buyer)
        if request.user.is_authenticated
        else []
    )

    return render(
        request,
        "chipi/index2.html",
        {"prod": products, "fav_prod": fav_prod, "search_text": search_query},
    )


def catg(request, cat_id):
    return render(
        request,
        "chipi/cats.html",
        context={
            "cat_id": cat_id,
        },
    )


def show_product_old(request, product_id):
    # return HttpResponse(f"PRODUCT {product_id}")
    product = get_object_or_404(Product, pk=product_id)
    photos = ProductImage.objects.filter(product=product)
    data = {
        "title": product.title,
        "product": product,
        "photos": photos,
    }
    return render(request, "chipi/product.html", context=data)


@login_required
def show_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    photos = ProductImage.objects.filter(product=product)
    reviews = Review.objects.filter(product=product)
    user_bought = Order.objects.filter(
        product=product, user=request.user.buyer, status=Order.Status.DELIVERED
    ).exists()

    if request.method == "POST" and user_bought:
        form = ReviewForm(request.POST, request.FILES)
        if (
            form.is_valid()
            and not Review.objects.filter(
                product=product, user=request.user.buyer
            ).exists()
        ):
            form.instance.user = request.user.buyer
            form.instance.product = product
            form.save()
    else:
        form = ReviewForm()

    return render(
        request,
        "chipi/product.html",
        {
            "title": product.title,
            "product": product,
            "photos": photos,
            "form": form,
            "reviews": reviews,
            "is_bought": user_bought,
            "rev_count": reviews.count(),
        },
    )

def show_shop(request, seller_id):
    shop = get_object_or_404(Shop, pk=seller_id)
    products = Product.objects.filter(shop_id=shop.pk)
    return render(request, "chipi/shop.html", context={"prod": products, "shop": shop})


# @login_required


from django.contrib import messages

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.count == 0:
        messages.error(request, "Товар закончился на складе.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

    cart, created = Cart.objects.get_or_create(
        user=request.user.buyer, product=product, defaults={"count": 1}
    )

    if not created:
        if cart.count < product.count:
            cart.count += 1
            cart.save()
        else:
            messages.warning(request, "Достигнуто максимальное количество товара в корзине.")

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))



def cart_add_ajax(request):
    product_id = request.POST.get("product_id")
    product = Product.objects.get(id=product_id)
    carts = Cart.objects.filter(user=request.user.buyer, product=product)
    if not carts.exists():
        Cart.objects.create(user=request.user.buyer, product=product, count=1)
        if int(product.count) <= 2:
            response_data = {
                "status": "success",
                "product_id": product.id,
                "last": True,
                "max": True,
            }
        else:
            response_data = {
                "status": "success",
                "product_id": product.id,
                "last": False,
                "max": True,}
    else:
        cart = carts.first()
        if int(product.count) <= int(cart.count) + 1:
            response_data = {
                "status": "success",
                "product_id": product.id,
                "last": True,
                "max": True,
            }
        else:
            response_data = {
                "status": "success",
                "product_id": product.id,
                "last": False,
                "max": True,
            }
        if int(product.count) > int(cart.count):
            cart.count += 1
            response_data["max"] = False

        cart.save()

    # response_data = {'status': 'success', 'product_id': product.id, 'aaa': 'bbb'}
    return JsonResponse(response_data)
    # return render('home')


def cart_delete(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def cart_decr(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    if cart.count != 1:
        cart.count -= 1
    cart.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def cart_decr_in_index(request, product_id):
    cart = Cart.objects.get(product_id=product_id, user=request.user.buyer)
    if cart.count != 1:
        cart.count -= 1
        cart.save()
    else:
        cart.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def cart_decr_in_index_ajax(request):
    product_id = request.POST.get("product_id")
    cart = Cart.objects.get(product_id=product_id, user=request.user.buyer)
    if cart.count != 1:
        cart.count -= 1
        cart.save()
    else:
        cart.delete()
    response_data = {"status": "success", "aaa": "bbb"}
    return JsonResponse(response_data)

#lab4

def clean_cart(user):
    carts = Cart.objects.filter(user=user).order_by("-time_created")
    new_cart = []
    
    for cart in carts:
        if cart.product.count == 0:
            cart.delete()
        elif cart.count > cart.product.count:
            cart.count = cart.product.count
            cart.save()
            new_cart.append(cart)
        else:
            new_cart.append(cart)
    
    return new_cart

def calculate_cart_totals(carts):
    total_count = sum(cart.count for cart in carts)
    total_sum = sum(cart.sum() for cart in carts)
    return total_count, total_sum


def show_cart(request):
    if not request.user.is_buyer:
        return HttpResponseNotFound("<h1>Корзина не доступна в режиме магазина</h1>") if request.user.is_shop else redirect("users:login")

    carts = clean_cart(request.user.buyer)
    total_count, total_sum = calculate_cart_totals(carts)

    return render(
        request, 
        "chipi/cart.html", 
        context={"products": carts, "total_count": total_count, "total_sum": total_sum}
    )


def create_order(request):
    if not request.user.is_buyer:
        return HttpResponseNotFound("<h1>Оформление заказа недоступно в режиме магазина</h1>") if request.user.is_shop else redirect("users:login")

    user = request.user
    initial_data = {
        "phone": user.buyer.phone,
        "email": user.buyer.email,
        "last_name": user.buyer.last_name,
        "first_name": user.buyer.first_name,
        "middle_name": user.buyer.middle_name,
    }

    form = AddressForm(instance=user.buyer.correct_address) if user.buyer.correct_address else AddressForm(initial=initial_data)

    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = user.buyer.correct_address
            if address:
                Address.objects.filter(pk=address.id).update(**form.cleaned_data)
            else:
                address = Address.objects.create(**form.cleaned_data, user=user.buyer)
                user.buyer.correct_address = address
                user.buyer.save()
            return redirect("create_order")

    carts = clean_cart(user.buyer)
    if not carts:
        return redirect("home")

    total_count, total_sum = calculate_cart_totals(carts)

    return render(
        request, 
        "chipi/create_order.html", 
        context={"products": carts, "total_count": total_count, "total_sum": total_sum, "form": form}
    )



def pay_order(request):
    if not request.user.is_buyer:
        return HttpResponseNotFound("<h1>Оформление заказа недоступно в режиме магазина</h1>") if request.user.is_shop else redirect("users:login")

    user = request.user
    carts = clean_cart(user.buyer)
    address = user.buyer.correct_address

    if not address:
        return redirect("users:address")
    
    if not carts:
        return redirect("home")

    form = PaymentTestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        for cart in carts:
            if cart.count > cart.product.count:
                form.add_error(None, "Количество доступных товаров изменилось")
                return redirect("pay_order")

        for cart in carts:
            cart.product.count -= cart.count
            cart.product.save()
            Order.objects.create(
                user=user.buyer, 
                product=cart.product, 
                shop=cart.product.shop,
                count=cart.count, 
                price=cart.product.price, 
                title=cart.product.title,
                first_name=address.first_name, 
                middle_name=address.middle_name, 
                last_name=address.last_name,
                email=address.email, 
                phone=address.phone, 
                country=address.country,
                region=address.region, 
                city=address.city, 
                index=address.index, 
                addr=address.addr,
            )
            cart.delete()

        return redirect("orders")

    total_count, total_sum = calculate_cart_totals(carts)

    return render(
        request, 
        "chipi/pay_order.html", 
        context={"total_count": total_count, "total_sum": total_sum, "form": form}
    )

#End_lab4

def add_fav(request, product_id):
    product = Product.objects.get(id=product_id)
    if (
        len(Favorite.objects.filter(user=request.user.buyer, product_id=product_id))
        == 0
    ):
        Favorite.objects.create(user=request.user.buyer, product=product)
    # request.user.buyer.favorite.add(product_id)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def rem_fav(request, product_id):
    fav = Favorite.objects.get(user=request.user.buyer, product=product_id)

    fav.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def show_favorites(request):
    if request.user.is_buyer:
        favs = (
            Product.objects.filter(favorite__user=request.user.buyer)
            .annotate(mark=Avg("reviews__score"))
            .order_by("id")
            .select_related("shop")
            .annotate(
                count_in_cart=Min(
                    "cart__count", filter=Q(cart__user=request.user.buyer)
                )
            )
        )
        return render(request, "chipi/favorites.html", context={"prod": favs})
    elif request.user.is_shop:
        return HttpResponseNotFound(
            "<h1>Список желаний не доступен в режиме магазина</h1>"
        )
    else:
        return redirect("users:login")


def show_orders(request):
    user = request.user
    if not user.is_authenticated:
        return redirect(reverse_lazy("users:login"))
    if not user.is_buyer:
        return HttpResponseNotFound("<h1>Страница не найдена</h1>")

    orders = Order.objects.filter(user=request.user.buyer).order_by("-time_created")

    return render(request, "chipi/orders.html", context={"orders": orders})


def show_orders_for_shop(request):
    user = request.user
    if not user.is_authenticated:
        return redirect(reverse_lazy("users:login"))
    if not user.is_shop:
        return HttpResponseNotFound("<h1>Страница не найдена</h1>")

    orders = Order.objects.filter(shop=request.user.shop).order_by("-time_created")

    return render(request, "chipi/orders_shop.html", context={"orders": orders})


def addprod(request):
    user = request.user

    if not user.is_shop:
        return HttpResponseNotFound("<h1>Страница не найдена</h1>")

    if request.method == "POST":
        form = AddProdForm(request.POST, request.FILES)

        if form.is_valid():
            # print(form.cleaned_data)
            try:
                prod = Product.objects.create(**form.cleaned_data, shop=user.shop)
                files = request.FILES.getlist("files")

                for f in files:
                    a = ProductImage(product=prod, image=f)
                    a.save()
                return redirect("home")
            except:
                form.add_error(None, "Ошибка добавления хз")

    else:
        form = AddProdForm()

    return render(
        request,
        "chipi/addprod.html",
        {
            "form": form,
        },
    )


def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    photos = ProductImage.objects.filter(product=product)

    # data = {
    #     'title': product.title,
    #     'product': product,
    # }

    user = request.user
    if not user.is_shop:
        return HttpResponseNotFound("<h1>Страница не найдена</h1>")
    if user.shop != product.shop:
        return HttpResponseNotFound("<h1>Страница не найдена</h1>")

    form = AddProdForm(instance=product)

    if request.method == "POST":
        form = AddProdForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            files = request.FILES.getlist("files")
            if len(files) > 0:
                prim = ProductImage.objects.filter(product=product)
                for pr in prim:
                    if os.path.isfile(pr.image.path):
                        os.remove(pr.image.path)
                    pr.delete()
            for f in files:
                a = ProductImage(product=product, image=f)
                a.save()
            return redirect(
                reverse_lazy("edit_product", kwargs={"product_id": product.id})
            )
    return render(
        request,
        "chipi/edit_product.html",
        {"form": form, "product": product, "photos": photos},
    )


def search(request):
    search_query = request.GET.get("q")
    min_pr = request.GET.get("min_price")
    max_pr = request.GET.get("max_price")
    ctgs = ProdCategory.objects.filter(parent=None)
    # products = Product.objects.filter(is_published=1)
    if request.user.is_authenticated and request.user.is_buyer:
        carts = Cart.objects.filter(user=request.user.buyer).order_by("-time_created")
        for cart in carts:
            if cart.product.count == 0:
                cart.delete()
            elif cart.count > cart.product.count:
                cart.count = cart.product.count
                cart.save()

        fav_prod = Product.objects.filter(favorite__user=request.user.buyer)
        if search_query == None:
            products = (
                Product.objects.annotate(mark=Avg("reviews__score"))
                .order_by("id")
                .select_related("shop")
                .annotate(
                    count_in_cart=Min(
                        "cart__count", filter=Q(cart__user=request.user.buyer)
                    )
                )
            )
        else:
            products = (
                Product.objects.filter(
                    title__icontains=search_query,
                    price__gte=min_pr or 0,
                    price__lte=max_pr or 10**9,
                )
                .annotate(mark=Avg("reviews__score"))
                .order_by("id")
                .select_related("shop")
                .annotate(
                    count_in_cart=Min(
                        "cart__count", filter=Q(cart__user=request.user.buyer)
                    )
                )
            )

    else:
        fav_prod = []
        if search_query == None:
            products = (
                Product.objects.annotate(mark=Avg("reviews__score"))
                .order_by("id")
                .select_related("shop")
            )
        else:
            products = (
                Product.objects.filter(
                    title__icontains=search_query,
                    price__gte=min_pr or 0,
                    price__lte=max_pr or 10**9,
                )
                .annotate(mark=Avg("reviews__score"))
                .order_by("id")
                .select_related("shop")
            )
    datacon = {
        "prod": products,
        "fav_prod": fav_prod,
        "search_text": search_query or "",
        "min_pr": min_pr or "",
        "max_pr": max_pr or "",
        "ctgs": ctgs,
    }
    # return render(request, 'chipi/index_with_score.html', context={"prod": products, "fav_prod": fav_prod})
    return render(request, "chipi/search.html", context=datacon)


def show_category(request, category_slug):
    category = get_object_or_404(ProdCategory, slug=category_slug)
    ctg = category
    children_categories = ctg.get_descendants(include_self=True)
    path = [
        ctg,
    ]
    search_query = request.GET.get("q")
    min_pr = request.GET.get("min_price")
    max_pr = request.GET.get("max_price")
    next_ctgs = ProdCategory.objects.filter(parent=category)
    while ctg.parent:
        ctg = ctg.parent
        path = [
            ctg,
        ] + path

    if request.user.is_authenticated and request.user.is_buyer:
        carts = Cart.objects.filter(user=request.user.buyer).order_by("-time_created")
        for cart in carts:
            if cart.product.count == 0:
                cart.delete()
            elif cart.count > cart.product.count:
                cart.count = cart.product.count
                cart.save()

        fav_prod = Product.objects.filter(
            favorite__user=request.user.buyer, prodcategory_id=category.pk
        )
        if search_query == None:
            products = (
                Product.objects.filter(prodcategory__in=children_categories)
                .annotate(
                    mark=Avg("reviews__score"),
                    count_in_cart=Min(
                        "cart__count", filter=Q(cart__user=request.user.buyer)
                    ),
                )
                .order_by("id")
                .select_related("shop")
            )
        else:
            products = (
                Product.objects.filter(
                    prodcategory__in=children_categories,
                    title__icontains=search_query,
                    price__gte=min_pr or 0,
                    price__lte=max_pr or 10**9,
                )
                .annotate(
                    mark=Avg("reviews__score"),
                    count_in_cart=Min(
                        "cart__count", filter=Q(cart__user=request.user.buyer)
                    ),
                )
                .order_by("id")
                .select_related("shop")
            )
    else:
        fav_prod = []
        if search_query == None:
            products = (
                Product.objects.filter(prodcategory__in=children_categories)
                .annotate(mark=Avg("reviews__score"))
                .order_by("id")
                .select_related("shop")
            )
        else:
            products = (
                Product.objects.filter(
                    prodcategory__in=children_categories,
                    title__icontains=search_query,
                    price__gte=min_pr or 0,
                    price__lte=max_pr or 10**9,
                )
                .annotate(mark=Avg("reviews__score"))
                .order_by("id")
                .select_related("shop")
            )

    # return render(request, 'chipi/index_with_score.html', context={"prod": products, "fav_prod": fav_prod})
    datacon = {
        "search_text": search_query or "",
        "min_pr": min_pr or "",
        "max_pr": max_pr or "",
        "ctgs": next_ctgs,
        "prod": products,
        "fav_prod": fav_prod,
        "path": path,
    }
    return render(request, "chipi/cats.html", context=datacon)


def rem_review(request, rev_id):
    user = request.user.buyer
    review = Review.objects.get(id=rev_id, user=user)
    review.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def edit_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    user = request.user
    if not user.is_shop:
        return HttpResponseNotFound("<h1>Страница не найдена</h1>")
    if user.shop != order.shop:
        return HttpResponseNotFound("<h1>Страница не найдена</h1>")

    form = EditOrderForm(instance=order)

    if request.method == "POST":
        form = EditOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("edit_order", kwargs={"order_id": order_id}))

    return render(request, "chipi/edit_order.html", {"form": form, "order": order})
