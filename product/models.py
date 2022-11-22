from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, Thumbnail

# Create your models here.
class AdditionalFeature(models.Model):
  name = models.CharField(max_length=50, unique=True)
  slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

  def __str__(self):
    return self.name

class Tag(models.Model):
  name = models.CharField(max_length=50, unique=True)
  slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return f'/product/tag/{self.slug}/'

class Category(models.Model):
  name = models.CharField(max_length=50, unique=True)
  slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return f'/product/category/{self.slug}/'

  class Meta:
    verbose_name_plural = 'Categories'

class Company(models.Model):
  name = models.CharField(max_length=50, unique=True)
  slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
  address = models.CharField(max_length=70)
  contact = models.CharField(max_length=50, unique=True)
  company_image = models.ImageField(upload_to='product/company/images/%Y/%m/%d/', blank=True)
  description = models.CharField(max_length=255, blank=True)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return f'/product/company/{self.slug}/'

  class Meta:
    verbose_name_plural = 'Companies'

class Product(models.Model):
  title = models.CharField(max_length=80)
  hook_text = models.CharField(max_length=100, blank=True)
  description = models.TextField()
  date = models.DateField(default=timezone.now, editable=True)
  product_image = models.ImageField(upload_to='product/product/images//%Y/%m/%d/', blank=True)
  detail_image = models.ImageField(upload_to='product/product/images/%Y/%m/%d/', blank=True)
  product_price = models.IntegerField()
  on_sale_price = models.IntegerField(null=True, blank=True)
  rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
  company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL)
  category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
  tags = models.ManyToManyField(Tag, blank=True)
  additional_feature = models.ForeignKey(AdditionalFeature, null=True, blank=True, on_delete=models.SET_NULL)

  def __str__(self):
    return f'[{self.pk}] {self.title}:: {self.product_price} : {self.company}'

  def get_absolute_url(self):
    return f'/product/{self.pk}/'

