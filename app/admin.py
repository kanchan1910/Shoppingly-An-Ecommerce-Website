from django.contrib import admin
from .models import Customer, Product, Cart, OrderPlaced, Wish


admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(OrderPlaced)
admin.site.register(Wish)
# Register your models here.
