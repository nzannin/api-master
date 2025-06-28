from rest_framework import serializers
from api.models import Product

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
       