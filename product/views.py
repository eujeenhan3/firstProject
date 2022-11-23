from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Company, Tag
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify

# Create your views here.
class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['product_image', 'detail_image', 'title', 'hook_text', 'product_price',
              'on_sale_price', 'rating', 'company', 'additional_feature', 'category',
              'description']

    template_name = 'product/product_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(ProductUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        response = super(ProductUpdate, self).form_valid(form)
        self.object.tags.clear()
        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(';', ',')
            tags_list = tags_str.split(',')
            for new_tag in tags_list:
                new_tag = new_tag.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=new_tag)
                if is_tag_created:
                    tag.slug = slugify(tag, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for tag in self.object.tags.all():
                tags_str_list.append(tag.name)
            context['tags_str_default'] = ';'.join(tags_str_list)
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Product.objects.filter(category=None).count
        return context

class ProductCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
  model = Product
  fields = ['date', 'product_image', 'detail_image', 'title', 'hook_text', 'product_price',
            'on_sale_price', 'rating', 'company', 'additional_feature', 'category',
            'description']

  def test_func(self):
      return self.request.user.is_superuser or self.request.user.is_staff

  def form_valid(self, form):
      current_user = self.request.user
      if current_user.is_authenticated and (current_user.is_superuser
                                            or current_user.is_staff):
          form.instance.author = current_user
          response = super(ProductCreate, self).form_valid(form)

          tags_str = self.request.POST.get('tags_str')
          if tags_str:
              tags_str = tags_str.strip()
              tags_str = tags_str.replace(';', ',')
              tags_list = tags_str.split(',')
              for new_tag in tags_list:
                  new_tag = new_tag.strip()
                  tag, is_tag_created = Tag.objects.get_or_create(name=new_tag)
                  if is_tag_created:
                      tag.slug = slugify(tag, allow_unicode=True)
                      tag.save()
                  self.object.tags.add(tag)
          return response
      else:
          return redirect('/product/')

  def get_context_data(self, *, object_list=None, **kwargs):
    context = super(ProductCreate, self).get_context_data()
    context['categories'] = Category.objects.all()
    context['no_category_post_count'] = Product.objects.filter(category=None).count()
    return context

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

  def get_context_data(self, *, object_list=None, **kwargs):
    context = super(ProductList, self).get_context_data()
    context['categories'] = Category.objects.all()
    context['no_category_post_count'] = Product.objects.filter(category=None).count
    context['companies'] = Company.objects.all()
    return context

def about_page(request):
  return render(request, 'product/about.html', {
    'categories': Category.objects.all(),
    'no_category_post_count': Product.objects.filter(category=None).count(),
    'companies': Company.objects.all()
  })

def new_items_page(request):
  new_items = Product.objects.all().order_by('-pk')[0:4]
  return render(request, 'product/product_list.html', {
    'new_items': new_items,
    'categories': Category.objects.all(),
    'no_category_post_count': Product.objects.filter(category=None).count()
  })

def popular_items_page(request):
  popular_items = Product.objects.filter(rating=5).order_by('-pk')
  return render(request, 'product/product_list.html', {
    'popular_items': popular_items,
    'categories': Category.objects.all(),
    'no_category_post_count': Product.objects.filter(category=None).count(),
    'companies': Company.objects.all()
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
    'no_category_post_count': Product.objects.filter(category=None).count(),
    'companies': Company.objects.all()
  })

def company_page(request, slug):
  company = Company.objects.get(slug=slug)
  product_list = Product.objects.filter(company=company).order_by('-pk')
  return render(request, 'product/product_list.html', {
    'company': company,
    'product_list': product_list,
    'categories': Category.objects.all(),
    'no_category_post_count': Product.objects.filter(category=None).count(),
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
    'no_category_post_count': Product.objects.filter(category=None).count(),
  })