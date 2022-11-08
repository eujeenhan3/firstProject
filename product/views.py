from django.shortcuts import render
from .models import Product
from django.views.generic import ListView, DetailView

# Create your views here.
class ProductDetail(DetailView):
  model = Product

class ProductList(ListView):
  model = Product
  ordering = '-pk'
