from django.contrib import admin
from .models import Product, Company, Category, Tag, AdditionalFeature

# Register your models here.
admin.site.register(Product)

class CompanyAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

admin.site.register(Company, CompanyAdmin)

class CategoryAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

admin.site.register(Tag, TagAdmin)

class AdditionalFeatureAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

admin.site.register(AdditionalFeature, AdditionalFeatureAdmin)