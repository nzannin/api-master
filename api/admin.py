from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

#from django.contrib import admin
from api.models import Order, OrderItem

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
    ]
    
admin.site.register(Order, OrderAdmin)
User = get_user_model()
admin.site.register(User, UserAdmin)
