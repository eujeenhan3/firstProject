from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

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
  address = models.CharField(max_length=50, unique=True)
  contact = models.CharField(max_length=50, unique=True)
  slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return f'/product/company/{self.slug}/'

  class Meta:
    verbose_name_plural = 'Companies'

class Product(models.Model):
  title = models.CharField(max_length=30)
  hook_text = models.CharField(max_length=100, blank=True)
  description = models.TextField()
  product_image = models.ImageField(upload_to='product/images/%Y/%m/%d/', blank=True)
  product_price = models.FloatField()
  on_sale_price = models.FloatField(null=True, blank=True)
  rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
  company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL)
  category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
  tags = models.ManyToManyField(Tag, blank=True)
  additional_feature = models.ForeignKey(AdditionalFeature, null=True, blank=True, on_delete=models.SET_NULL)

  def __str__(self):
    return f'[{self.pk}] {self.title}:: {self.product_price} : {self.company}'

  def get_absolute_url(self):
    return f'/product/{self.pk}/'

