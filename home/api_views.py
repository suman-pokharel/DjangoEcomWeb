from .models import *
from .serializers import *
from rest_framework import  viewsets
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend




class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends=[DjangoFilterBackend]
    lookup_field=['name']
    
