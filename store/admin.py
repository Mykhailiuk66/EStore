from django.contrib import admin
from . import models

admin.site.register(models.ShopUser)
admin.site.register(models.Product)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.ShippingInfo)


