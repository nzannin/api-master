from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

#from django.contrib import admin
from api.models import Order, OrderItem, User, Product

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
    ]


class ProductAdmin(admin.ModelAdmin):
    model = Product


admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(User, UserAdmin)

