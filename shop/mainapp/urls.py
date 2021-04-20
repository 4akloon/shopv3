from django.urls import path
from . import views as v
from . import api

urlpatterns = [
    path('', v.BaseView.as_view(), name='base'),
    path('category/<str:slug>', v.CategoryView.as_view(), name='category'),
    path('product/<str:slug>', v.ProductDetailView.as_view(), name='product_detail'),
    path('review/<int:pk>/', v.AddReview.as_view(), name='add_review'),
    path('favorites', v.FavoritesView.as_view(), name='favorites'),
    path('favorite/<int:id>', v.Like.as_view(), name='favorite'),
    path('cart', v.CartView.as_view(), name='cart'),
    path('add_to_cart/<int:id>', v.AddToCartView.as_view(), name='add_to_cart'),
    path('delete_from_cart/<int:id>', v.DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change_cartproduct_count/<int:id>', v.ChangeCountView.as_view() ,name='change_cartproduct_count'),

    path('api/category', api.CategoryAPIView.as_view(), name='category_api'),
    path('api/category/<str:slug>', api.CategoryDetailAPIView.as_view(), name='category_detail_api'),
    path('api/products', api.ProductsAPIView.as_view(), name='products_api'),
    path('api/favorites', api.FavoritesAPIView.as_view(), name='favorites_api'),
    path('api/products/<int:id>', api.ProductDetailAPIView.as_view(), name='product_detail_api'),
    path('api/products/<int:id>/images', api.ProductImagesAPIView.as_view(), name='product_images_api'),
    path('api/products/<int:id>/reviews', api.ProductReviewsAPIView.as_view(), name='reviews_api'),
    path('api/cart', api.CartProductsAPIView.as_view(), name='cart_api'),
    path('api/cart/<int:id>', api.CartProductAPIView.as_view(), name='cartproduct_api'),
    path('api/favorite/<int:id>', api.LikeAPIView.as_view(), name='like_api'),
    path('api/reviews', api.ReviewsAPIView.as_view(), name='reviews_api'),
    path('api/reviews/<int:id>', api.ReplyReviewsAPIView.as_view(), name='reply_reviews_api'),
]

