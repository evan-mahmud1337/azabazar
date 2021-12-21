from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import ProductSerializer, CategorySerializer, OfferSerializer
from products.models import Products, Category, Offers


class LatestProductView(APIView):
    def get(self, request, format=None):
        product = Products.objects.all()[:8]
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)

class AllproductView(APIView):
    def get(self, request, format=None):
        product = Products.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)
class OfferView(APIView):
    def get(self, request, format=None):
        products = Offers.objects.all()
        serializer = OfferSerializer(products, many=True)
        return Response(serializer.data)

class CategoryView(APIView):
    def get(self, request, format=None):
        catagory = Category.objects.all()
        serializer =  CategorySerializer(catagory, many=True)
        return Response(serializer.data)

@api_view(['POST'], )
def search(request):
    q = request.data.get('q', '')
    products =  Products.objects.filter(Q(title__icontains=q) | Q(description__icontains=q))
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
