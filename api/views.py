from django.db.models import Max
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from api.filters import InStockFilterBackend, OrderFilter, ProductFilter
from api.models import Order, OrderItem, Product, User
from api.serializers import (OrderCreateSerializer, OrderSerializer,
                             ProductInfoSerializer, ProductSerializer,
                             UserSerializer)
from rest_framework.throttling import ScopedRateThrottle
from api.tasks import send_order_confirmation_email


class ProductListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list all products or create a new product.
    Supports GET and POST methods.
    Post only by administrators
    """
    throttle_scope = 'products'  # This is used for throttling requests to this view
    throttle_classes = [ScopedRateThrottle] # This allows for scoped throttling based on the 'products' scope
    
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

    @method_decorator(cache_page(60 * 15, key_prefix='product_list'))  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        """
        Handle GET requests to list products.
        No additional logic is needed here, as the caching decorator handles it.
        """
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        import time
        time.sleep(2)  # Simulate a delay for chaching demonstration purposes
        return super().get_queryset()

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
    throttle_scope = 'orders'   # This is used for throttling requests to this viewset
    throttle_classes = [ScopedRateThrottle] # This allows for scoped throttling based on the 'orders' scope
        
    queryset = Order.objects.order_by('pk').prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None         # !!!!!!!! to disable default pagination for this viewset
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]
    
    
    def perform_create(self, serializer):
        """
        Override to set the user to the authenticated user when creating an order.
        """
        order = serializer.save(user=self.request.user)
        # Send an email confirmation after the order is created (Celery task)
        # This is an asynchronous task to avoid blocking the request/response cycle
        send_order_confirmation_email.delay(order.order_id, self.request.user.email)
        
    
    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the request method.
        """
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return OrderCreateSerializer
        return OrderSerializer
    
    
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            # If the user is not an admin, filter orders by the authenticated user
            return qs.filter(user=self.request.user)
        return qs
    
    # @action(detail=False, methods=['get'], url_path='user-orders', permission_classes=[IsAuthenticated])
    # def user_orders(self, request):
    #     """
    #     Custom action to list orders for the authenticated user.
    #     """        
    #     orders = self.queryset.filter(user=request.user)
    #     serializer = self.get_serializer(orders, many=True)
    #     return Response(serializer.data)


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


class UserListView(generics.ListAPIView):
    """
    API view to list all users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None  # Disable pagination for this view    

