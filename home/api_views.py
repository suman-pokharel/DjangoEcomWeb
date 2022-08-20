from .models import *
from .serializers import *
from rest_framework import  viewsets
from rest_framework.generics import ListAPIView




class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # filter_backends=[DjangoFilterBackend]
    # lookup_field=['stock']
    # filterset_fields = ['stock']
    
