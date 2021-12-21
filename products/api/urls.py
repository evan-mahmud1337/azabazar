from products.api.serializers import OfferSerializer
from django.urls import path
from django.urls.resolvers import URLPattern
from . import views
# from .views import LatestProductView, AllproductView, OfferView, CategoryView

urlpatterns = [
    path('latest-product/', views.LatestProductView.as_view(), name='latest-product'),
    path('all-products/', views.AllproductView.as_view(), name='all-products'),
    path('categories/', views.CategoryView.as_view(), name='categories'),
    path('offers/', views.OfferView.as_view(), name='offers'),
    path('search/', views.search, name='search'),
]