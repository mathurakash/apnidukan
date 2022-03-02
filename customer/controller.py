from django.urls import path
from . import views
app_name='customer'

urlpatterns = [
    path('',views.Home.as_view(),name="main"),
    path('home',views.AddToCart,name="AddToCart"),
    path('AddToCart/<int:pk>',views.AddToCart,name='AddToCart'),
    path("customer_signup",views.Register.as_view(),name="c-signup"),
    path("customer_signin",views.LoginPage.as_view(),name="c-signin"),
    path('logout/',views.signout,name="logout"),
    path("subcat/<int:pk>",views.Detailpage.as_view(),name='detail'),
    path("subcat/product/<int:pk>",views.Productpage.as_view(),name='prod'),
    path("subcat/product/buy/<int:pk>",views.Buy.as_view(),name='buy'),

    
    # path('subcat/product/buy/payment/',views.pay,name="pay"),

        path('success',views.success,name="success")
    
]