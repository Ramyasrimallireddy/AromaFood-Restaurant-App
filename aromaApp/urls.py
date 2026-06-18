from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index),
    path('open_signup',views.open_signup,name = 'open_signup'),
    path('open_signin',views.open_signin,name = 'open_signin'),
    path('signup',views.signup,name = 'signup'),
    path('signin',views.signin,name = 'signin'),
    path('open_add_restuarant',views.open_add_restuarant,name = 'open_add_restuarant'),   
    path('add_restuarant',views.add_restuarant,name = 'add_restuarant'),
    path('open_show_restuarant',views.open_show_restuarant,name = 'open_show_restuarant'),
    path('open_update_restuarant/<int:restuarant_id>', views.open_update_restuarant, name='open_update_restuarant'),
    path('update_restuarant/<int:restuarant_id>', views.update_restuarant, name='update_restuarant'),
    path('view_menu/<int:restuarant_id>/<str:username>/', views.view_menu, name='view_menu'),
    path('update_menu/<int:restuarant_id>/', views.update_menu, name='update_menu'),
    path('open_update_menu/<int:restuarant_id>/', views.open_update_menu, name='open_update_menu'),
    path('delete_restuarant/<int:restuarant_id>/', views.delete_restuarant, name='delete_restuarant'),
    path('add_to_cart/<int:item_id>/<str:username>', views.add_to_cart, name='add_to_cart'), 
    path('show_cart/<str:username>', views.show_cart, name='show_cart'), 
    path('checkout/<str:username>/', views.checkout, name='checkout'),
    path('orders/<str:username>/', views.orders, name='orders'),
]