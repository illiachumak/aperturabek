from django.contrib import admin
from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ['name']

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'categoryId', 'price', 'isAvailable')
    search_fields = ['title', 'categoryId__name']

class ModificationsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'type')
    search_fields = ['name', 'type__name']

class ModificationsTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

class ColorPhotosAdmin(admin.ModelAdmin):
    list_display = ('color','product')
    search_fields = ['color__name', 'product__title']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Modifications, ModificationsAdmin)
admin.site.register(ModificationType, ModificationsTypeAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(ImagesForColor, ColorPhotosAdmin)
