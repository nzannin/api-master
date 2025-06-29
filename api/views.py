from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, OrderItemSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView



class ProductListAPIView(generics.ListAPIView):
    """
    API view to list all products.
    """
    queryset = Product.objects.filter(stock__gt=0)
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    """
    API view to retrieve a single product by its ID.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


class OrderListAPIView(generics.ListAPIView):
    """
    API view to list all orders.
    """
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer


class UserOrderListAPIView(generics.ListAPIView):
    """
    API view to list all orders for a specific user.
    """
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Override to filter orders by the authenticated user.
        """
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
    

class ProductInfoAPIView(APIView):
    """
    API view to get product information, including count and max price.
    """     
    def get(self, request):
        """
        Handle GET requests to retrieve product information.
        """
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(Max('price'))['price__max']
        })
        
        return Response(serializer.data)
    
