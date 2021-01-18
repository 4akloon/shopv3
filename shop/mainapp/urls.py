from django.urls import path

from .views import *

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('category/<str:slug>/', CategoryView.as_view(), name='category'),
    path('product/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('review/<int:pk>/', AddReview.as_view(), name='add_review'),
]
