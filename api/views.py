from django.db.models import Max
from api.serializers import ProductSerializer, OrderSerializer, OrderItemSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from api.filters import ProductFilter



class ProductListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list all products or create a new product.
    Supports GET and POST methods.
    Post only by administrators
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    def get_permissions(self):
        self.permission_classes = [AllowAny] 
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
            
        return super().get_permissions()


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve a single product by its ID, update it, or delete it.
    Supports GET, PUT, PATCH, and DELETE methods.
    PUT, PATCH, and DELETE methods are restricted to administrators.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    
    def get_permissions(self):
        self.permission_classes = [AllowAny] 
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
            
        return super().get_permissions()


class OrderListAPIView(generics.ListAPIView):
    """
    API view to list all orders.
    """
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]


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
    

class ProductInfoAPIView(generics.ListAPIView):
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
    
