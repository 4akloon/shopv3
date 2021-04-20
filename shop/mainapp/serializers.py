from rest_framework import serializers
from .models import *
from djoser import serializers as dj_serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    state = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Product
        exclude = ('draft',)

class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class UserCreateSerializer(dj_serializers.UserCreateSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User._meta.pk.name,
            User.USERNAME_FIELD,
            "password",
            'first_name', 
            'last_name'
        )

class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartProduct
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'


class CustomerSerilizer(serializers.ModelSerializer):
    user = CurrentUserSerializer()
    class Meta:
        model = Customer
        exclude = ['favorites']


class ReviewsSerializer(serializers.ModelSerializer):
    customer = CustomerSerilizer()
    product = ProductSerializer()
    class Meta:
        model = Reviews
        fields = '__all__'

