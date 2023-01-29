from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.utils import timezone
import json
from .models import Product, Order, ShopUser, OrderItem
from .forms import ContactInfoForm

def get_card_data(request):
    if request.user.is_anonymous:
        try:
            orderCart = json.loads(request.COOKIES["order"])
        except:
            orderCart = {}

        
        order = {'get_order_total': 0, 'get_order_quantity': 0}
        order_items = []
        for itemId, quantity in orderCart.items():
            product = Product.objects.get(id=itemId)
            get_total = product.price * quantity

            order["get_order_quantity"] += quantity
            order["get_order_total"] += quantity * product.price
            order_items.append({
                "product": product, 
                "quantity": quantity,
                "get_total": get_total
                })
    else:
        shop_user = request.user.shopuser
        order, created = Order.objects.get_or_create(
            customer=shop_user, ordered=None, complete=False
        )
        order_items = order.orderitem_set.all()
        
    return order, order_items


def handle_purchase(request, form):
    if form.is_valid():
        if request.user.is_anonymous:
            contactInfoForm = ContactInfoForm(request.POST)
            if contactInfoForm.is_valid():
                try:
                    user = User.objects.get(
                        email=contactInfoForm.cleaned_data['email'],
                        first_name=contactInfoForm.cleaned_data['first_name'],
                        last_name=contactInfoForm.cleaned_data['last_name'],
                                                        )
                    print('User does exist, please log in')
                    return redirect('cart')
                except:
                    shop_user, created = ShopUser.objects.get_or_create(
                        email=contactInfoForm.cleaned_data['email'],
                    )
                    shop_user.first_name = contactInfoForm.cleaned_data['first_name']
                    shop_user.last_name = contactInfoForm.cleaned_data['last_name']
                    shop_user.save()
                    
                    order = Order.objects.create(
                        customer=shop_user, ordered=None, complete=False
                    )
                    
                    cart = json.loads(request.COOKIES.get('order', '{}'))
                    
                    for itemId, quantity in cart.items():
                        product = Product.objects.get(id=itemId)
                        OrderItem.objects.create(
                            product=product,
                            order=order,
                            quantity=quantity
                            )
        else:
            shop_user = request.user.shopuser
            order, created = Order.objects.get_or_create(
                customer=shop_user, ordered=None, complete=False
            )

        print(order.get_order_quantity)
        if order.get_order_quantity < 1:
            return redirect('cart')
        
        shipping_info = form.save(commit=False)
        shipping_info.customer = shop_user
        shipping_info.order = order
        shipping_info.save()

        order.ordered = timezone.now()
        order.complete = True
        order.save()