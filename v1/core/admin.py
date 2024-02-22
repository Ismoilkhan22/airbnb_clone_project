from django.contrib import admin

from .models import  Product, Image, Amenities, Conditions

from v1.core.category import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", 'status')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "region", "name", "description", "price", "price_currency", "status",  "category")

@admin.register(Image)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "product")



@admin.register(Amenities)
class AmenitiesAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Conditions)
class ConditionsAdmin(admin.ModelAdmin):
    list_display = ("id", "amenity", "title")
