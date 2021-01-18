from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms

from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Product
        fields = '__all__'


class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 0
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" height="150"/>')

    get_image.short_description = 'Изображение'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_image', 'category', 'url', 'state', 'draft')
    list_filter = ('category', 'state')
    search_fields = ('title', 'category__name', 'state__name')
    inlines = [ProductImagesInline]
    save_on_top = True
    list_editable = ('draft',)
    readonly_fields = ('get_image',)
    form = ProductAdminForm

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="100"/>')

    get_image.short_description = 'Изображение'


@admin.register(StateProduct)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'product', 'date')
    search_fields = ('name', 'email', 'date', 'text', 'parent__name')
    readonly_fields = ('name', 'email')


admin.site.site_title = 'AppStore'
admin.site.site_header = 'AppStore'
