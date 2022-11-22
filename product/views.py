from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Company, Tag
from django.views.generic import ListView, DetailView

# Create your views here.
class ProductDetail(DetailView):
  model = Product

  def get_context_data(self, **kwargs):
    context = super(ProductDetail, self).get_context_data()
    context['related_products'] = Product.objects.filter(category_id=self.object.category_id).order_by('-pk')[0:4]
    context['related_products_count'] = Product.objects.filter(category_id=self.object.category_id).count()-1
    context['categories'] = Category.objects.all()
    context['no_category_post_count'] = Product.objects.filter(category=None).count()
    context['companies'] = Company.objects.all()
    return context

class ProductList(ListView):
  model = Product
  ordering = 'pk'

  def get_context_data(self, *, object_list=None, **kwargs):
    context = super(ProductList, self).get_context_data()
    context['categories'] = Category.objects.all()
    context['no_category_post_count'] = Product.objects.filter(category=None).count
    context['companies'] = Company.objects.all()
    return context

def new_items_page(request):
  new_items = Product.objects.all().order_by('-pk')[0:4]
  return render(request, 'product/product_list.html', {
    'new_items': new_items,
    'categories': Category.objects.all()
  })

def popular_items_page(request):
  popular_items = Product.objects.filter(rating=5).order_by('-pk')
  return render(request, 'product/product_list.html', {
    'popular_items': popular_items,
    'categories': Category.objects.all()
  })

def category_page(request, slug):
  if slug == 'no_category':
    category = 'etc'
    product_list = Product.objects.filter(category=None).order_by('-pk')
  else:
    category = Category.objects.get(slug=slug)
    product_list = Product.objects.filter(category=category).order_by('-pk')
  return render(request, 'product/product_list.html', {
    'category': category,
    'product_list': product_list,
    'categories': Category.objects.all(),
    'no_category_post_count': Product.objects.filter(category=None).count
  })

def company_page(request, slug):
  company = Company.objects.get(slug=slug)
  product_list = Product.objects.filter(company=company).order_by('-pk')
  return render(request, 'product/product_list.html', {
    'company': company,
    'product_list': product_list,
    'categories': Category.objects.all(),
    'companies': Company.objects.all()
  })

def tag_page(request, slug):
  tag = Tag.objects.get(slug=slug)
  product_list = tag.product_set.all().filter(tags=tag).order_by('-pk')
  return render(request, 'product/product_list.html', {
    'tag': tag,
    'product_list': product_list,
    'no_tag_product_count': Product.objects.filter(tags=None).count,
    'categories': Category.objects.all(),
  })