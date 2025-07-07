from django.db.models import Max
from api.serializers import ProductSerializer, OrderSerializer, OrderItemSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from api.filters import ProductFilter, InStockFilterBackend
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination




class ProductListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list all products or create a new product.
    Supports GET and POST methods.
    Post only by administrators
    """
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend
        ]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'stock']
    # pagination_class = PageNumberPagination
    # pagination_class.page_size = 2
   

    # to use a diffrente parameter for pagination number just add the following
    # pagination_class.page_query_param = 'page_number'
    
    
    # if you want the client to be able to manage pagination size just add the following
    # pagination_class.page_size_query_param = 'size'
    # pagination_class.max_page_size = 1000

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

##### commented when introduced viewsets #######

# class OrderListAPIView(generics.ListAPIView):
#     """
#     API view to list all orders.
#     """
#     queryset = Order.objects.order_by('pk').prefetch_related('items__product')
#     serializer_class = OrderSerializer
#     permission_classes = [IsAdminUser]
    
    
# class UserOrderListAPIView(generics.ListAPIView):
#     """
#     API view to list all orders for a specific user.
#     """
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         """
#         Override to filter orders by the authenticated user.
#         """
#         qs = super().get_queryset()
#         return qs.filter(user=self.request.user)
    

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage orders.
    Supports listing, retrieving, creating, updating, and deleting orders.
    """
    queryset = Order.objects.order_by('pk').prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    pagination_class = None         # to disable pagination for this viewset



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
    
