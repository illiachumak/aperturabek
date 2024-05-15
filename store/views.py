from rest_framework import viewsets
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.db.models import Q
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.http import Http404


# Create your views here.

class CustomPaginator(PageNumberPagination):
    page_size = 12
    page_query_param = 'page'

class CategoryViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPaginator
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    http_method_names = ['get',]
    
    
    def list(self, request):
        query = self.queryset.filter(parent=None)
        serializer = CategorySerializer(query, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        params = request.query_params
        sub_categories = list(Category.objects.filter(parent = pk).values_list('id', flat=True))
        products = Product.objects.filter(Q(categoryId = pk) | Q(categoryId__in = sub_categories) & Q(isAvailable = True))
        prices = list(products.values_list('price', flat=True))
        try:
            products = products.filter(Q(price__range=(params['min'], params['max'])))
        except:
            pass
        try:
            if params['sort'] == 'priceup':
                products = products.order_by('price')
            elif params['sort'] == 'pricedown':
                products = products.order_by('-price')
        except:
            pass 
        if len(prices) == 0:
            prices = [0] 
        page = self.paginate_queryset(products)
        serializer = ProductsSerializer(page, many=True)
        name = Category.objects.filter(id = pk).first().name    
        context = {"name": name, "products": serializer.data,  'min_price': min(prices), 'max_price':max(prices)}
        return self.get_paginated_response(context)
        
    
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductWithPhotosSerializer
    queryset = Product.objects.all()
    http_method_names = ['get',]

    def retrieve(self, request, pk=None):
        query = get_object_or_404(Product, pk = pk, isAvailable = True)
        serializer = ProductWithPhotosSerializer(query)
        return Response(serializer.data)
    

@api_view(["GET"])
def return_ok(request):
    return Response(status=status.HTTP_200_OK)