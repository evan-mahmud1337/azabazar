from products.api.serializers import OfferSerializer
from django.urls import path
from django.urls.resolvers import URLPattern
from . import views
# from .views import LatestProductView, AllproductView, OfferView, CategoryView

urlpatterns = [
    path('latest-product/', views.LatestProductView.as_view(), name='latest-product'),
    path('all-products/', views.AllproductView.as_view(), name='all-products'),
    path('exclusive-products/', views.ExclusiveproductView.as_view(), name='exclusive-products'),
    path('categories/', views.CategoryView.as_view(), name='categories'),
    path('offers/', views.OfferView.as_view(), name='offers'),
    path('offersimage/', views.OfferImageView.as_view(), name='offersimage'),
    path('search/', views.search, name='search'),
    path('catagorisedproduct/<id>/', views.catwisepro, name='catwise'),
]