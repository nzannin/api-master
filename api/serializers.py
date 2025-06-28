from rest_framework import serializers
from api.models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
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
    
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, obj):
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
