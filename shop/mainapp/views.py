from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required




from .forms import *
from .models import *
from .filters import ProductFilter



class BaseView(View):

    def get(self, request):
        context = {}
        return render(request, 'base.html', context)


class ProductsView(ListView):
    model = Product
    queryset = Product.objects.all()
    template_name = 'products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())
        return context


class CategoryView(ListView):
    model = Category
    template_name = 'products.html'

    def get(self, request, slug):
        context = {}
        category = Category.objects.get(url=slug)
        context['category'] = category
        context['product_list'] = Product.objects.filter(category=category)
        context['filter'] = ProductFilter(self.request.GET, queryset=context['product_list'])
        return render(request, 'products.html', context)


class ProductDetailView(DetailView):
    model = Product
    slug_field = 'url'
    template_name = 'product_detail.html'

    def get(self, request, slug):
        context = {}
        context['product'] = Product.objects.get(url=slug)
        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user)
            if Product.objects.get(url=slug) in customer.favorites.get_queryset():
                context['liked'] = True
            else:
                context['liked'] = False
            carts = Cart.objects.filter(status=2, customer=customer)
            for cart in carts:
                for prod in cart.get_products():
                    if prod.product == context['product']:
                        context['bought'] = True
            if not 'bought' in context:
                context['bought'] = False
        return render(request, 'product_detail.html', context)


class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        product = Product.objects.get(id=pk)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.product = product
            form.customer = customer
            carts = Cart.objects.filter(status=2, customer=customer)
            for cart in carts:
                for prod in cart.get_products():
                    if prod.product == product:
                        form.bought = True
            form.save()
        return redirect(product.get_absolute_url())


class FavoritesView(ListView):
    model = Product
    template_name = 'favorites.html'

    def get(self, request):
        customer = Customer.objects.get(user=request.user)
        context = {}
        context['product_list'] = customer.favorite_set.all()
        return render(request, 'favorites.html', context)


class CartView(View):

    def get(self, request):
        customer = Customer.objects.get(user=request.user)
        context = {}
        context['cart'] = customer.cart_set.get(status=1)
        return render(request, 'cart.html', context)


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(request=request, username=form.cleaned_data.get("username"), password=form.clean_password2())
            login(request, user)
            customer = Customer(user=user)
            customer.save()
            cart = Cart(customer=customer)
            cart.save()
        return redirect('/')
    else:
        form = CreateUserForm()

    return render(request, 'register.html', {'form': form})


class Like(View):

    def post(self, request, id):
        product = Product.objects.get(id=id)
        customer = Customer.objects.get(user=request.user)
        if not Favorite.objects.filter(product=product, customer=customer):
            Favorite.objects.create(product=product, customer=customer).save()
        else:
            ob = Favorite.objects.filter(product=product, customer=customer)
            ob.delete()
        return redirect(product.get_absolute_url())


class AddToCartView(View):

    def get(self, request, id):
        product = Product.objects.get(id=id)
        customer = Customer.objects.get(user=request.user)
        cart = customer.cart_set.get(status=1)
        cart_product, created = CartProduct.objects.get_or_create(parent=cart, product=product)
        return redirect('/cart')

class DeleteFromCartView(View):

    def get(self, request, id):
        cart_product = CartProduct.objects.get(id=id)
        cart_product.delete()
        return redirect('/cart')

class ChangeCountView(View):

    def post(self, request, id):
        customer = Customer.objects.get(user=request.user)
        cart = customer.cart_set.get(status=1)
        cart_product = CartProduct.objects.get(id=id)
        if cart_product.parent.customer == customer:
            count = int(request.POST.get('count'))
            cart_product.count = count
            cart_product.save()
        return redirect('/cart')



# def error_404_view(request, exeption):
#     return render('404.html')
