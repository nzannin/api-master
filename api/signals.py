from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from api.models import Product
from django.core.cache import cache

@receiver([post_save, post_delete], sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    """
    Invalidate the product list cache when a Product is created, updated, or deleted.
    """
    cache_key = '*product_list*'  # Use a wildcard or specific key if needed
    cache.delete_pattern(cache_key)
    print(f"Cache for {cache_key} invalidated due to {kwargs.get('signal', 'unknown')} signal.")    