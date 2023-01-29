from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.StoreView.as_view(), name='store'),
    path('product/<str:pk>', views.ProductView.as_view(), name='product'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('update-item/', views.UpdateItemQuantityView.as_view(), name='update-item'),
    path('orders/', views.OrdersView.as_view(), name='orders'),
    path('create-product/', views.CreateProductView.as_view(), name='create-product'),
    
    
    
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    

]
