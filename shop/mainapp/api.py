from django.http import HttpResponseNotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, generics

import ast

from .serializers import *


class CategoryAPIView(APIView):

    def get(self, request):

        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True )
        return Response(serializer.data)


class CategoryDetailAPIView(APIView):

    def get(self, request, slug):
        try:
            category = Category.objects.get(url=slug)
            products = Product.objects.filter(category=category).reverse()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Exception:
            return Response(status=404)


class ProductDetailAPIView(APIView):

    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Exception:
            return Response(status=404)


class ProductsAPIView(APIView):

    def get(self, request):
        try:
            products = Product.objects.all().order_by('-id')
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Exception:
            return Response(status=404)

class FavoritesAPIView(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):
        try:
            customer = Customer.objects.get(user=request.user)
            products = customer.favorites.get_queryset().order_by('-id')
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Exception:
            return Response(status=404)

class CartProductsAPIView(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):
        customer = Customer.objects.get(user=request.user)
        cart = customer.cart_set.get(status=1)
        cartproducts = cart.cartproduct_set.all()
        serializer = CartProductSerializer(cartproducts, many=True)
        return Response(serializer.data)

class CartProductAPIView(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def put(self, request, id):
        customer = Customer.objects.get(user=request.user)
        cart = customer.cart_set.get(status=1)
        cart_product = CartProduct.objects.get(id=id)
        if cart_product.parent.customer == customer:
            count = ast.literal_eval(request.body.decode("UTF-8"))['count']
            cart_product.count = count
            cart_product.save()
            return Response(status=200)
        return Response(status=404)


    def post(self, request, id):
        try:
            product = Product.objects.get(id=id)
            customer = Customer.objects.get(user=request.user)
            cart = customer.cart_set.get(status=1)
            cart_product, created = CartProduct.objects.get_or_create(parent=cart, product=product)
            return Response(status=200)
        except Exception:
            return Response(status=404)


    def delete(self, request, id):
        try:
            cart_product = CartProduct.objects.get(id=id)
            cart_product.delete()
            return Response(status=200)
        except Exception:
            return Response(status=404)

class LikeAPIView(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
            customer = Customer.objects.get(user=request.user)
            if not Favorite.objects.filter(product=product, customer=customer):
                return Response(status=202)
            else:
                return Response(status=201)
        except Exception:
            return Response(status=404)

    def post(self, request, id):
        try:
            product = Product.objects.get(id=id)
            customer = Customer.objects.get(user=request.user)
            Favorite.objects.create(product=product, customer=customer).save()
            return Response(status=200)
        except Exception:
            return Response(status=404)

    def delete(self, request, id):
        try:
            product = Product.objects.get(id=id)
            customer = Customer.objects.get(user=request.user)
            ob = Favorite.objects.filter(product=product, customer=customer).order_by('-id')
            ob.delete()
            return Response(status=200)
        except Exception:
            return Response(status=404)

class ProductImagesAPIView(APIView):

    def get(self, request, id):
        product = Product.objects.get(id=id)
        images = product.productimages_set.all().order_by('-id')
        serializer = ProductImageSerializer(images, many=True)
        return Response(serializer.data)

class ProductReviewsAPIView(APIView):

    def get(self, request, id):
        product = Product.objects.get(id=id)
        reviews = product.reviews_set.filter(parent__isnull=True).order_by('-date')
        serializer = ReviewsSerializer(reviews, many=True)
        return Response(serializer.data)

class ReplyReviewsAPIView(APIView):

    def get(self, request, id):
        review = Reviews.objects.get(id=id)
        reviews = review.reviews_set.all().order_by('-date')
        serializer = ReviewsSerializer(reviews, many=True)
        return Response(serializer.data)

class ReviewsAPIView(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def post(self, request):
        print(request.body)
        customer = Customer.objects.get(user=request.user)
        product = Product.objects.get(id=request.data['product'])
        carts = Cart.objects.filter(status=2, customer=customer)
        bought = False
        for cart in carts:
            for prod in cart.get_products():
                if prod.product == product:
                    bought = True
        text = request.data['text']
        if request.data['parent']:
            parent = Reviews.objects.get(id=request.data['parent'])
        else: 
            parent = None
        Reviews.objects.create(customer=customer, product=product, parent=parent, text=text, bought=bought).save()
        print(request.data)
        return Response(status=200)