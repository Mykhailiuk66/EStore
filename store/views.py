from django.shortcuts import render, redirect, resolve_url
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
import json
from .models import Product, Order, OrderItem, ShopUser
from .forms import CustomUserLoginForm, CustomUserCreationForm, ShippingInfoForm, ContactInfoForm, ProductCreationForm
from .utils import get_card_data, handle_purchase


@method_decorator(ensure_csrf_cookie, name="dispatch")
class StoreView(ListView):
    model = Product
    template_name = "store/store.html"
    context_object_name = "products"
    paginate_by = 6
    ordering = ["-created"]

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search")

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )

        return queryset


class ProductView(DetailView):
    template_name = "store/single-product.html"
    model = Product


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CartView(View):
    def get(self, request):
        order, order_items = get_card_data(request)

        form = ShippingInfoForm()
        contactInfoForm = ContactInfoForm()
        context = {"order": order, "order_items": order_items, "form": form, 'contactInfoForm': contactInfoForm}
        return render(request, "store/cart.html", context=context)

    def post(self, request):
        form = ShippingInfoForm(request.POST)
        handle_purchase(request, form)

        if request.user.is_anonymous:
            response = HttpResponseRedirect(resolve_url('store'))
            response.delete_cookie('order') 
                
            return response
        else:            
            return redirect("orders")


class OrdersView(LoginRequiredMixin, ListView):
    template_name = "store/orders.html"
    model = Order
    context_object_name = "orders"

    def get_queryset(self):
        query_set = super().get_queryset()

        customer = self.request.user.shopuser
        query_set = query_set.filter(customer=customer).exclude(ordered__isnull=True)
        return query_set


class UpdateItemQuantityView(View):
    def post(self, request):
        data = json.loads(request.body)
        product_id = data["productId"]
        action = data["action"]

        shop_user = request.user.shopuser
        product = Product.objects.get(id=product_id)
        order, created = Order.objects.get_or_create(
            customer=shop_user, ordered=None, complete=False
        )
        order_item, created = OrderItem.objects.get_or_create(
            order=order, product=product
        )

        if action == "add":
            order_item.quantity = order_item.quantity + 1
        elif action == "remove":
            order_item.quantity = order_item.quantity - 1

        order_item.save()

        if order_item.quantity <= 0:
            order_item.delete()

        return JsonResponse("Item was updated", safe=False)


class UserLoginView(LoginView):
    template_name = "store/login_register.html"
    form_class = CustomUserLoginForm
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "Sign In"
        return context


class UserRegisterView(CreateView):
    template_name = "store/login_register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "Sign Up"
        return context

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("store")
        return super().dispatch(*args, **kwargs)


class CreateProductView(PermissionRequiredMixin, CreateView):
    permission_required = 'store.add_product'

    template_name = "form.html"
    form_class = ProductCreationForm
    success_url = reverse_lazy('store')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'New Product'
        
        return context
        
        
        