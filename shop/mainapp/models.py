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
        verbose_name = 'Состояние'
        verbose_name_plural = 'Состояния'


class Product(models.Model):

    title = models.CharField('Название', max_length=150)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='products/')
    category = models.ForeignKey(Category, verbose_name='Карегория', on_delete=models.SET_NULL, null=True)
    price = models.IntegerField('Цена')
    state = models.ForeignKey(StateProduct, verbose_name='Состояние', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160)
    draft = models.BooleanField('Черновик', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.url})

    def get_reviews(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ProductImages(models.Model):

    image = models.ImageField('Изображение', upload_to='product_images/')
    description = models.TextField('Описание')
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товара'


class Reviews(models.Model):

    email = models.EmailField()
    name = models.CharField('Имя', max_length=100)
    text = models.TextField('Сообщение',max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.product}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
