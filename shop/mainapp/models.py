from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):

    name = models.CharField('Категория', max_length=100)
    description = models.TextField('Описание')
    icon = models.ImageField('Иконка', upload_to='category_icon/')
    url = models.SlugField(max_length=160)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.url})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class StateProduct(models.Model):

    name = models.CharField('Имя', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Состояние товара'
        verbose_name_plural = 'Состояния товаров'


class Product(models.Model):

    title = models.CharField('Название', max_length=150)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='products/')
    category = models.ForeignKey(
        Category, verbose_name='Карегория', on_delete=models.SET_NULL, null=True)
    price = models.IntegerField('Цена')
    state = models.ForeignKey(
        StateProduct, verbose_name='Состояние', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160)
    draft = models.BooleanField('Черновик', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.url})

    def get_reviews(self):
        return self.reviews_set.filter(parent__isnull=True)

    def get_fav(self, user):
        print(111)
        customer = Customer.objects.get(user=user)
        if Product.objects.get(id=self.id) in customer.favorites.get_queryset():
            print(1)
            return True
        else:
            print(2)
            return False

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ProductImages(models.Model):

    image = models.ImageField('Изображение', upload_to='product_images/')
    description = models.TextField('Описание')
    product = models.ForeignKey(
        Product, verbose_name='Продукт', on_delete=models.CASCADE)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товара'


class CartStatus(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус корзины'
        verbose_name_plural = 'Статусы корзин'


class Customer(models.Model):

    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE)
    favorites = models.ManyToManyField(
        Product, verbose_name='Избранное', blank=True, through='Favorite')
    address = models.CharField(
        verbose_name='Адресс', max_length=150, blank=True, null=True)
    number = models.CharField(
        'Номер телефона', max_length=14, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_full_name(self):
        return self.user.first_name + ' ' + self.user.last_name

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Cart(models.Model):

    customer = models.ForeignKey(
        Customer, verbose_name='Пользователь', on_delete=models.CASCADE)
    status = models.ForeignKey(
        CartStatus, verbose_name='Статус', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.customer.user.username + ' ' + self.status.name

    def get_full_price(self):
        price = 0
        for item in self.cartproduct_set.all():
            price = price + item.get_price()
        return price

    def get_products(self):
        return self.cartproduct_set.all()

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartProduct(models.Model):

    product = models.ForeignKey(
        Product, verbose_name='Продукт', on_delete=models.CASCADE)
    count = models.PositiveIntegerField(verbose_name='Количество', default=1)
    parent = models.ForeignKey(
        Cart, verbose_name='Корзина', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def get_price(self):
        return self.product.price * self.count

    class Meta:
        verbose_name = 'Товар из корзины'
        verbose_name_plural = 'Товары из корзины'


class OrderStatus(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta: 
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, verbose_name='Пользователь', on_delete=models.CASCADE)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, verbose_name='Корзина')
    status = models.ForeignKey(
        OrderStatus, on_delete=models.SET_DEFAULT, default=1)
    address = models.CharField(max_length=300, verbose_name='Адресс')
    final_price = models.IntegerField('Общая цена')
    paid = models.BooleanField('Оплачено', default=False)
    comment = models.CharField(max_length=100)
    created_at = models.DateTimeField(
        auto_now=True, verbose_name='Дата создания заказа')

    def __str__(self):
        return self.cart.customer.user.username + ' ' + self.status.name

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Favorite(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer.user.username + ' ' + self.product.title

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        unique_together = [['product', 'customer']]


class Reviews(models.Model):

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, verbose_name='Покупатель')
    text = models.TextField('Сообщение', max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(
        Product, verbose_name='Продукт', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    bought = models.BooleanField(default=False, verbose_name='Купил')

    def __str__(self):
        return f"{self.customer} - {self.product}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
