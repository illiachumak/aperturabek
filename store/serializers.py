from rest_framework import serializers
from .models import *
from django.db.models import Q

class SubSerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories']
        
    def get_subcategories(self,obj):
        data = SubSerializer(Category.objects.filter(parent = obj), many=True).data
        return data
    

class ModOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modifications
        fields = ['id', 'name', 'price', 'image']

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleImages
        fields = ['image']

class ImagePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagesForColor
        fields = ("image",)
    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data['image'] = data['image'].split('?')[0]
        return data

class ColorSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    def get_image(self, obj):
        product_id = int(self.context.get("product_id"))
        return ImagePhotoSerializer(ImagesForColor.objects.filter(Q(color=obj) & Q(product=product_id)), many=True).data

    class Meta:
        model = Color
        fields = ['id', 'name','preview_image', 'image'] 

    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data['preview_image'] = data['preview_image'].split('?')[0]
        return data

        

class ModificationSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    def get_options(self, obj):
        return ModOptionsSerializer(Modifications.objects.filter(type = obj.id), many=True).data
    class Meta:
        model = ModificationType
        fields = ['name', 'options']

class ProductsSerializer(serializers.ModelSerializer):
    modifications = serializers.SerializerMethodField()
    def get_modifications(self, obj):
        return ModificationSerializer(ModificationType.objects.filter(product = obj), many=True).data
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'image_preview', 'modifications']

    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data['image_preview'] = data['image_preview'].split('?')[0]
        return data


class ProductWithPhotosSerializer(serializers.ModelSerializer):
    modifications = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    colors = serializers.SerializerMethodField()
    categoryId = serializers.StringRelatedField()

    def get_modifications(self, obj):
        return ModificationSerializer(ModificationType.objects.filter(product = obj), many=True).data
    
    def get_photos(self,obj):
        return PhotoSerializer(MultipleImages.objects.filter(product = obj), many=True).data
    
    def get_colors(self,obj):
        return ColorSerializer(Color.objects.filter(product = obj), many=True, context={'product_id':obj.id}).data
    
    class Meta:
        model = Product
        fields = ['id', 'title','price', 'image_preview', 'description', 'categoryId', 'modifications', 'photos', 'colors']

    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data['image_preview'] = data['image_preview'].split('?')[0]
        return data

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    def get_subcategories(self, obj):
        return SubSerializer(Category.objects.filter(parent=obj), many=True).data
    class Meta:
        model = Category
        fields = ['id', 'name','preview_image', 'subcategories']

    def to_representation(self, instance):
        data =  super().to_representation(instance)
        try:
            data['preview_image'] = data['preview_image'].split('?')[0]
        except:
            pass
        return data

class CategoryProductsSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    def get_products(self,obj):
        return ProductsSerializer(obj)
    class Meta:
        model = Product
        fields = ['products']

   
