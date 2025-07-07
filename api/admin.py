from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

#from django.contrib import admin
from api.models import Order, OrderItem, User

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
    ]
    
admin.site.register(Order, OrderAdmin)
admin.site.register(User, UserAdmin)
