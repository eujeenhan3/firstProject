from django.urls import path
from . import views

urlpatterns=[ #IP주소/blog
    path('', views.ProductList.as_view()),
    path('<int:pk>/', views.ProductDetail.as_view())
]