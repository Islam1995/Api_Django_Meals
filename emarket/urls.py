from django.urls import path
from . import views

urlpatterns =[
    path('products/', views.get_all_products, name='all_products'),
    path('products/<slug:slug>/', views.get_product_by_slug, name='product'),
    path('products/new', views.new_product, name='new_product'),
    path('products/update/<str:pk>/', views.update_product, name='update_product'),
    path('products/delete/<str:pk>/', views.delete_product, name='delete_product'),
    path('<str:pk>/review/', views.create_review, name='create_review'),
]