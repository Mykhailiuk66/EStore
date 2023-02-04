from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from uuid import uuid4

# Create your models here.


class ShopUser(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(max_length=250, unique=True, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)
    
    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)


class Product(models.Model):
    name = models.CharField(max_length=1000, blank=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default='default.png', null=True, blank=True)
    slug = models.SlugField(max_length=1000, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        base_slug = slugify(self.name)
        unique_slug = base_slug
        suffix = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{suffix}"
            suffix += 1
        self.slug = unique_slug
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(
        ShopUser, on_delete=models.SET_NULL, null=True, blank=True
    )
    ordered = models.DateTimeField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    @property
    def get_order_quantity(self):
        order_items = self.orderitem_set.all()
        quantity = sum([item.quantity for item in order_items])

        return quantity

    @property
    def get_order_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])

        return total

    def __str__(self):
        return self.customer.first_name + ' ' + self.customer.last_name + ' - ' + str(self.id)
    
    class Meta:
        ordering = ['-ordered']
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)
    
    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total

    def __str__(self):
        return str(self.order.id) + ' - ' + str(self.product.name) + ' - ' + str(self.quantity)
    

class ShippingInfo(models.Model):
    customer = models.ForeignKey(ShopUser, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=500, blank=False, null=False)
    address = models.CharField(max_length=500, blank=False, null=False)
    zipcode = models.CharField('Zip code', max_length=100, blank=False, null=False)
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)
    
    def __str__(self):
        return str(self.id)
    
    