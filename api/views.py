from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer
from api.models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def product_list(request):
    """
    View to list all products.
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request, pk):
    """
    View to retrieve a single product by its ID.
    """
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)