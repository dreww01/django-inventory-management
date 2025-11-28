from django.urls import path
from . import views

urlpatterns =[

    path('', views.home_view, name='home_view'),
    path('create/', views.product_create_view, name='product_create_view'),
    path('list/', views.product_list_view, name='product_list_view'),
    path('update/<int:pk>', views.product_update_view, name='product_update_view'),
    path('delete/<int:pk>', views.product_delete_view, name='product_delete_view'),
]