from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

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
        context['product_list'] = Product.objects.filter(category=category)
        context['filter'] = ProductFilter(self.request.GET, queryset=context['product_list'])
        return render(request, 'products.html', context)


class ProductDetailView(DetailView):
    model = Product
    slug_field = 'url'
    template_name = 'product_detail.html'


class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        product = Product.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.product = product
            form.save()
        return redirect(product.get_absolute_url())

