from django.urls import path
from . import views

urlpatterns=[
    path('', views.ProductList.as_view()),
    path('<int:pk>/', views.ProductDetail.as_view()),
    path('category/<str:slug>/', views.category_page),
    path('company/<str:slug>/', views.company_page),
    path('popular_items/', views.popular_items_page),
    path('tag/<str:slug>/', views.tag_page),
    path('new_arrivals/', views.new_items_page),
]
