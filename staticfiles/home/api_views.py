from .models import *
from .serializers import *
from rest_framework import  viewsets



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
