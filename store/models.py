from collections.abc import Iterable
from typing import Any
from django.db import models
from django.utils.timezone import datetime
from io import BytesIO
from PIL import Image
from django.core.files import File
from os import path
from django.utils import timezone
import uuid


def compress(image):
        im = Image.open(image)
        im_io = BytesIO() 
        im = im.convert("RGB")
        im = im.save(im_io,format='WEBP', quality=80)
        image_name = custom_name(image)
        print(image.name)
        new_image = File(im_io, name=image_name)
        return new_image

def custom_name(image):
    _,ext  = path.splitext(image.name)
    return f'image_{uuid.uuid4().hex}.webp'


class ModificationType(models.Model):
    name = models.CharField(max_length=100, unique = True)

    class Meta:
        db_table = 'Modifications'

    def __str__(self) -> str:
        return self.name
    
class Modifications(models.Model):
    name    = models.CharField(max_length=200, unique = True)
    price   = models.DecimalField(max_digits=10, decimal_places=2)
    type    = models.ForeignKey(ModificationType, blank=True, null = True, on_delete = models.CASCADE)
    image   = models.ImageField(upload_to='', blank=True, null=True)

    class Meta:
        db_table = 'Options for modification'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        try:
            new_image = compress(self.image)
            self.image = new_image
        except:
            pass
        super().save(*args, **kwargs)
    
class Color(models.Model):
    name            = models.CharField(max_length=100, unique = True)
    preview_image   = models.ImageField(upload_to='')

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name    = models.CharField(max_length=100, unique=True)
    parent  = models.ForeignKey('self', blank=True, on_delete=models.CASCADE, null=True)
    preview_image = models.ImageField(blank=True)

    class Meta:
        db_table = 'Product_categories'

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        try:
            new_image = compress(self.preview_image)
            self.preview_image = new_image
        except:
            pass
        super().save(*args, **kwargs)


    

    
class Product(models.Model):
    title               = models.CharField(max_length=250)
    description         = models.TextField(max_length=1000)
    price               = models.DecimalField(max_digits=10, decimal_places=2)
    categoryId          = models.ForeignKey(Category, related_name=("products"), on_delete=models.CASCADE)
    image_preview       = models.ImageField(null=True)
    modifications       = models.ManyToManyField(ModificationType, blank=True)
    color               = models.ManyToManyField(Color, blank=True)
    isAvailable         = models.BooleanField(default=True) 

    class Meta:
        db_table = 'Products'

    def __str__(self) -> str:
        return self.title

    
    def save(self, *args, **kwargs):
        try:
            new_image = compress(self.image_preview)
            self.image_preview = new_image
        except:
            pass
        super().save(*args, **kwargs)



class MultipleImages(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    image       = models.ImageField(upload_to='', blank=True, null=True)

    class Meta:
        db_table = 'Product_images'

    def __str__(self) -> str:
        return self.product.title
    
    def save(self, *args, **kwargs):
        try:
            new_image = compress(self.image)
            self.image = new_image
        except:
            pass
        super().save(*args, **kwargs)
    
class ImagesForColor(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    color       = models.ForeignKey(Color, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='')

    def __str__(self) -> str:
        return self.color.name
    
    def save(self, *args, **kwargs):
        try:
            new_image = compress(self.image)
            self.image = new_image
        except:
            pass
        super().save(*args, **kwargs)
