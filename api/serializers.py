
from django.db import transaction
from rest_framework import serializers
from api.models import Product, Order, OrderItem, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
#        fields = '__all__'  # bad practice, consider specifying fields explicitly
#        exclude = ('password', 'user_permission')  # Ebad practice, consider specifying fields explicitly
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'orders'    # Assuming you want to include related orders (see related_name in User model)
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name',
            'description',
            'price',
            'stock',
        )

    def validate_price(self, value):
        """
        Validate that the price is a positive number.
        """
        if value < 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return value
 

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source='product.price', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = (
            'product_name',
            'product_price',
            'quantity',
            'item_subtotal',
        )
 
        
class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = (
                'product',
                'quantity',
            )   
    
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemCreateSerializer(many=True, required=False)
    
    def create(self, validated_data):
        """
        Create an Order instance along with its associated OrderItems.
        """
        items_data = validated_data.pop('items')
        
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            
            for item_data in items_data:
                OrderItem.objects.create(order=order, **item_data)
        
        return order
    
    def update(self, instance, validated_data):
        """
        Update an Order instance and its associated OrderItems.
        """
        items_data = validated_data.pop('items', None)
        
        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if items_data is not None:
                # Clear existing items if new items are provided
                instance.items.all().delete()
                # Create new items
                for item_data in items_data:
                    OrderItem.objects.create(order=instance, **item_data)
        
        return instance
                
    class Meta:
        model = Order
        fields = (
            'order_id',
            'user',
            'status',
            'items',
        )
        extra_kwargs = {
            'user': {'read_only': True}
        }
    
 
    
class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, obj) -> float:
        """
        Calculate the total price of the order by summing the subtotals of each item.
        """
        return sum(item.item_subtotal for item in obj.items.all())
    
    class Meta:
        model = Order
        fields = (
            'order_id',
            'user',
            'created_at',
            'status',
            'items',
            'total_price',
        )
        
        
class ProductInfoSerializer(serializers.Serializer):
    """
    Serializer for getting all products, count of products, max_price
    """
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
