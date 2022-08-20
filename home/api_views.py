from .models import *
from .serializers import *
from rest_framework import  viewsets
from django_filters.rest_framework import DjangoFilterBackend
import django_filters.rest_framework
from rest_framework import generics




class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # filter_backends=[DjangoFilterBackend]
    # lookup_field=['name']
    filterset_fields = ['category', 'in_stock']
    
